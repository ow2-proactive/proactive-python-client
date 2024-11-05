"""
ProActive Node Metrics Monitor

A tool for monitoring ProActive node metrics including:
- System resources (CPU, Memory, Load)
- Heap and Non-Heap memory usage
- Thread statistics
- Custom alerting thresholds

Usage:
    python -m proactive.monitoring.ProActiveNodeMetricsMonitor [--debug] [--continuous] [--interval SECONDS]
"""

import humanize
import argparse
import requests
import time
from datetime import datetime
from proactive import getProActiveGateway
from proactive.monitoring.ProactiveNodeMBeanClient import MBeanObjectNames

class ProActiveNodeMetricsMonitor:
    def __init__(self, gateway, node_url="service:jmx:ro:///jndi/pamr://4097/rmnode", debug=False):
        """
        Initialize the metrics monitor
        
        Args:
            gateway: ProActive gateway instance
            node_url: JMX URL for the node to monitor
            debug: Whether to show debug output
        """
        self.gateway = gateway
        self.debug = debug
        
        # Ensure proper base URL configuration
        base_url = gateway.getBaseURL()
        self.base_url = f"{base_url}/rest" if not base_url.endswith('/rest') else base_url
        self.session_id = gateway.getSession()
        self.node_url = node_url
        
        # Default thresholds - can be customized
        self.thresholds = {
            'cpu_high': 0.80,     # 80% CPU usage
            'memory_high': 0.90,  # 90% memory usage
            'thread_high': 200    # 200 threads
        }

    def _make_request(self, endpoint, params):
        """Make an authenticated request to the ProActive REST API"""
        url = f"{self.base_url}{endpoint}"
        headers = {"sessionid": self.session_id}
        
        if self.debug:
            print(f"\nDEBUG: Making request to {url}")
            print(f"DEBUG: Headers: {headers}")
            print(f"DEBUG: Params: {params}")
        
        response = requests.get(url, headers=headers, params=params)
        
        if self.debug:
            print(f"DEBUG: Response status: {response.status_code}")
            print(f"DEBUG: Response URL: {response.url}")
            if not response.ok:
                print(f"DEBUG: Response text: {response.text}")
            
        response.raise_for_status()
        return response.json()

    def format_bytes(self, bytes_value):
        """Format bytes to human readable string"""
        return humanize.naturalsize(bytes_value, binary=True)

    def format_percentage(self, value):
        """Format value as percentage"""
        return f"{value * 100:.2f}%"

    def format_memory_usage(self, memory_info):
        """Format memory usage information"""
        return {
            'Initial': self.format_bytes(memory_info['init']),
            'Used': self.format_bytes(memory_info['used']),
            'Committed': self.format_bytes(memory_info['committed']),
            'Max': self.format_bytes(memory_info['max']) if memory_info['max'] != -1 else 'No limit',
            'Usage': f"{(memory_info['used'] / memory_info['committed'] * 100):.1f}%"
        }

    def get_node_metrics(self, metrics, attributes=None):
        """
        Get metrics from node MBeans
        
        Args:
            metrics: List of MBean object names
            attributes: Optional list of specific attributes to retrieve
        """
        params = {
            "nodejmxurl": self.node_url,
            "objectname": ",".join(metrics)
        }
        if attributes:
            params["attrs"] = attributes
            
        return self._make_request("/rm/node/mbeans", params)

    def get_metrics_snapshot(self):
        """Get a snapshot of all monitored metrics"""
        metrics = {}
        
        # Get OS metrics
        os_metrics = self.get_node_metrics(
            metrics=[MBeanObjectNames.OPERATING_SYSTEM],
            attributes=["SystemCpuLoad", "ProcessCpuLoad", "SystemLoadAverage", 
                       "FreePhysicalMemorySize", "TotalPhysicalMemorySize"]
        )
        
        for item in os_metrics[MBeanObjectNames.OPERATING_SYSTEM]:
            if item['name'] == 'SystemCpuLoad':
                metrics['system_cpu'] = item['value']
            elif item['name'] == 'ProcessCpuLoad':
                metrics['process_cpu'] = item['value']
            elif item['name'] == 'SystemLoadAverage':
                metrics['load_avg'] = item['value']
            elif item['name'] == 'FreePhysicalMemorySize':
                metrics['free_memory'] = item['value']
            elif item['name'] == 'TotalPhysicalMemorySize':
                metrics['total_memory'] = item['value']

        # Get memory metrics
        memory_metrics = self.get_node_metrics(
            metrics=[MBeanObjectNames.MEMORY],
            attributes=["HeapMemoryUsage", "NonHeapMemoryUsage"]
        )
        
        memory_data = memory_metrics[MBeanObjectNames.MEMORY]
        for item in memory_data:
            if item['name'] == 'HeapMemoryUsage':
                metrics['heap_used'] = item['value']['used']
                metrics['heap_max'] = item['value']['max']
                metrics['heap_info'] = self.format_memory_usage(item['value'])
            elif item['name'] == 'NonHeapMemoryUsage':
                metrics['nonheap_info'] = self.format_memory_usage(item['value'])

        # Get thread metrics
        thread_metrics = self.get_node_metrics(
            metrics=[MBeanObjectNames.THREADING],
            attributes=["ThreadCount", "PeakThreadCount", "TotalStartedThreadCount"]
        )
        
        thread_data = thread_metrics[MBeanObjectNames.THREADING]
        for item in thread_data:
            metrics[item['name'].lower()] = item['value']

        return metrics

    def print_metrics(self, metrics, show_alerts=True):
        """Print metrics in a formatted way"""
        print(f"\nMetrics Snapshot at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        if show_alerts:
            alerts = []
            if metrics['system_cpu'] > self.thresholds['cpu_high']:
                alerts.append(f"HIGH CPU USAGE: {self.format_percentage(metrics['system_cpu'])}")
            
            memory_used_ratio = metrics['heap_used'] / metrics['heap_max']
            if memory_used_ratio > self.thresholds['memory_high']:
                alerts.append(f"HIGH MEMORY USAGE: {self.format_percentage(memory_used_ratio)}")
            
            if metrics['threadcount'] > self.thresholds['thread_high']:
                alerts.append(f"HIGH THREAD COUNT: {metrics['threadcount']}")
            
            if alerts:
                print("\nALERTS:")
                for alert in alerts:
                    print(f"⚠️  {alert}")
                print("-" * 60)

        print("\nSystem Resources:")
        print(f"CPU Usage (System)............. {self.format_percentage(metrics['system_cpu'])}")
        print(f"CPU Usage (Process)............ {self.format_percentage(metrics['process_cpu'])}")
        print(f"System Load Average............ {metrics['load_avg']:.2f}")
        print(f"Physical Memory Usage.......... {self.format_bytes(metrics['total_memory'] - metrics['free_memory'])} / {self.format_bytes(metrics['total_memory'])}")

        print("\nHeap Memory Usage:")
        for key, value in metrics['heap_info'].items():
            print(f"{key:.<30} {value}")

        print("\nNon-Heap Memory Usage:")
        for key, value in metrics['nonheap_info'].items():
            print(f"{key:.<30} {value}")

        print("\nThread Statistics:")
        print(f"Current Thread Count........... {metrics['threadcount']}")
        print(f"Peak Thread Count.............. {metrics['peakthreadcount']}")
        print(f"Total Started Threads.......... {metrics['totalstartedthreadcount']}")

def main():
    parser = argparse.ArgumentParser(description='Monitor ProActive node metrics')
    parser.add_argument('--debug', action='store_true', help='Show debug output')
    parser.add_argument('--continuous', action='store_true', help='Enable continuous monitoring')
    parser.add_argument('--interval', type=float, default=5.0,
                       help='Interval between metric updates in seconds (default: 5.0)')
    args = parser.parse_args()

    print("Initializing ProActive gateway...")
    gateway = getProActiveGateway()

    try:
        # Create monitor instance
        monitor = ProActiveNodeMetricsMonitor(gateway, debug=args.debug)
        
        if args.continuous:
            print(f"\nStarting continuous monitoring (interval: {args.interval}s)")
            print("Press Ctrl+C to stop monitoring")
            try:
                while True:
                    metrics = monitor.get_metrics_snapshot()
                    monitor.print_metrics(metrics)
                    time.sleep(args.interval)
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user")
        else:
            metrics = monitor.get_metrics_snapshot()
            monitor.print_metrics(metrics)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        if hasattr(e, 'response'):
            print("Response status code:", getattr(e.response, 'status_code', 'N/A'))
            print("Response text:", getattr(e.response, 'text', 'N/A'))
            if hasattr(e.response, 'url'):
                print("Request URL:", e.response.url)
    finally:
        gateway.close()
        print("\nDisconnected and finished.")

if __name__ == "__main__":
    main()

"""
(env) ➜  proactive-python-client git:(master) ✗ python -m proactive.monitoring.ProActiveNodeMetricsMonitor
Initializing ProActive gateway...
Logging on proactive-server...
Connecting on: https://try.activeeon.com:8443
Connected

Metrics Snapshot at 2024-11-05 14:12:10
------------------------------------------------------------

System Resources:
CPU Usage (System)............. 3.06%
CPU Usage (Process)............ 1.61%
System Load Average............ 0.01
Physical Memory Usage.......... 34.1 GiB / 62.7 GiB

Heap Memory Usage:
Initial....................... 1004.0 MiB
Used.......................... 48.7 MiB
Committed..................... 383.5 MiB
Max........................... 13.9 GiB
Usage......................... 12.7%

Non-Heap Memory Usage:
Initial....................... 2.4 MiB
Used.......................... 123.5 MiB
Committed..................... 133.2 MiB
Max........................... No limit
Usage......................... 92.7%

Thread Statistics:
Current Thread Count........... 72
Peak Thread Count.............. 285
Total Started Threads.......... 125590

Disconnected and finished.
"""
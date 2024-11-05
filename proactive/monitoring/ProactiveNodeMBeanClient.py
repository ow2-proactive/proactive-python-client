import requests
import logging
import json
from typing import List, Dict, Any, Optional, Union
from enum import Enum

logger = logging.getLogger('ProactiveNodeMBeanClient')

class MBeanObjectNames:
    """Constants for commonly used MBean object names"""
    OPERATING_SYSTEM = "java.lang:type=OperatingSystem"
    MEMORY = "java.lang:type=Memory"
    THREADING = "java.lang:type=Threading"
    CLASS_LOADING = "java.lang:type=ClassLoading"
    CPU_CORE_USAGE = "sigar:Type=CpuCoreUsage,Name=*"
    FILE_SYSTEM = "sigar:Type=FileSystem,Name=*"
    CPU_USAGE = "sigar:Type=CpuUsage"
    MEMORY_USAGE = "sigar:Type=Mem"
    NETWORK_INTERFACE = "sigar:Type=NetInterface,Name=*"
    SWAP = "sigar:Type=Swap"

class TimeRange(Enum):
    """Time range options for historical data"""
    MINUTE_1 = 'a'   # 1 minute
    MINUTE_5 = 'n'   # 5 minutes
    MINUTE_10 = 'm'  # 10 minutes
    MINUTE_30 = 't'  # 30 minutes
    HOUR_1 = 'h'     # 1 hour
    HOUR_2 = 'j'     # 2 hours
    HOUR_4 = 'k'     # 4 hours
    HOUR_8 = 'H'     # 8 hours
    DAY_1 = 'd'      # 1 day
    WEEK_1 = 'w'     # 1 week
    MONTH_1 = 'M'    # 1 month
    YEAR_1 = 'y'     # 1 year

class JMXProtocol(Enum):
    """Supported JMX connection protocols"""
    RMI = "rmi"  # For direct RMI connections
    RO = "ro"    # For read-only PAMR connections

class CPUMetric(Enum):
    """CPU metrics that can be collected"""
    USER = "User"           # CPU time spent in user mode
    SYSTEM = "Sys"         # CPU time spent in system mode
    NICE = "Nice"          # CPU time spent on nice priorities
    IDLE = "Idle"          # CPU idle time
    WAIT = "Wait"          # CPU time spent in wait (I/O)
    IRQ = "Irq"            # CPU time spent servicing interrupts
    SOFT_IRQ = "SoftIrq"   # CPU time spent servicing soft interrupts
    STOLEN = "Stolen"      # CPU time stolen by other domains
    COMBINED = "Combined"  # Combined CPU utilization

class MemoryMetric(Enum):
    """Memory metrics that can be collected"""
    USED = "Used"                 # Memory currently in use
    TOTAL = "Total"               # Total available memory
    FREE = "Free"                 # Free memory
    USED_PERCENT = "UsedPercent"  # Percentage of memory used
    RAM = "Ram"                   # Total RAM
    ACTUAL_USED = "ActualUsed"    # Actual memory in use
    FREE_PERCENT = "FreePercent"  # Percentage of memory free
    ACTUAL_FREE = "ActualFree"    # Actual free memory

class ProactiveNodeMBeanClient:
    """Client for accessing node monitoring information through JMX MBeans."""

    def __init__(self, gateway, node_url: str = "service:jmx:ro:///jndi/pamr://4097/rmnode"):
        """Initialize the Node MBean client."""
        self.gateway = gateway
        self.node_url = node_url
        self._base_url = f"{gateway.getBaseURL()}/rest"

    def _make_request(self, endpoint: str, params: dict) -> dict:
        """Make authenticated request to ProActive REST API."""
        headers = {"sessionid": self.gateway.getSession()}
        url = f"{self._base_url}{endpoint}"
        
        logger.debug(f"Making request to {url} with params {params}")
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def _get_metrics(self, 
                    metrics: List[str], 
                    attributes: Optional[List[str]] = None,
                    historical: bool = False,
                    time_range: TimeRange = TimeRange.MINUTE_5) -> dict:
        """Get metrics from specified MBeans."""
        endpoint = "/rm/node/mbeans/history" if historical else "/rm/node/mbeans"
        
        params = {
            "nodejmxurl": self.node_url,
            "objectname": ",".join(metrics)
        }
        
        if attributes:
            params["attrs"] = ",".join(attributes)
            
        if historical:
            params["range"] = time_range.value
            
        return self._make_request(endpoint, params)

    def _parse_historical_data(self, response: dict, mbean_name: str, key_format: str) -> List[float]:
        """Parse historical data from response."""
        try:
            if mbean_name in response:
                data = json.loads(response[mbean_name])
                if key_format in data:
                    return [float(value) for value in data[key_format]]
        except json.JSONDecodeError:
            logger.error(f"Failed to parse historical data for {mbean_name}")
        except Exception as e:
            logger.error(f"Error parsing historical data: {e}")
        return []

    def get_cpu_metrics(self, 
                       metric: CPUMetric = CPUMetric.COMBINED,
                       historical: bool = False, 
                       time_range: TimeRange = TimeRange.MINUTE_5) -> Union[float, List[float]]:
        """Get CPU usage metrics."""
        try:
            if historical:
                response = self._get_metrics(
                    metrics=[MBeanObjectNames.CPU_USAGE],
                    attributes=[metric.value],
                    historical=True,
                    time_range=time_range
                )
                values = self._parse_historical_data(
                    response, 
                    MBeanObjectNames.CPU_USAGE,
                    f"{metric.value}CpuUsage"
                )
                return [v * 100 for v in values]
            else:
                response = self._get_metrics(
                    metrics=[MBeanObjectNames.CPU_USAGE],
                    attributes=[metric.value]
                )
                if MBeanObjectNames.CPU_USAGE in response:
                    data = response[MBeanObjectNames.CPU_USAGE]
                    if isinstance(data, list):
                        for item in data:
                            if item['name'] == metric.value:
                                return item['value'] * 100
                return 0.0
        except Exception as e:
            logger.error(f"Error getting CPU metric {metric.value}: {e}")
            return [] if historical else 0.0

    def get_memory_metrics(self, 
                         metric: MemoryMetric = MemoryMetric.USED_PERCENT,
                         historical: bool = False,
                         time_range: TimeRange = TimeRange.MINUTE_5) -> Union[float, List[float]]:
        """Get memory usage metrics."""
        try:
            if historical:
                response = self._get_metrics(
                    metrics=[MBeanObjectNames.MEMORY_USAGE],
                    attributes=[metric.value],
                    historical=True,
                    time_range=time_range
                )
                values = self._parse_historical_data(
                    response, 
                    MBeanObjectNames.MEMORY_USAGE,
                    f"{metric.value}Mem"
                )
                return values
            else:
                response = self._get_metrics(
                    metrics=[MBeanObjectNames.MEMORY_USAGE],
                    attributes=[metric.value]
                )
                if MBeanObjectNames.MEMORY_USAGE in response:
                    data = response[MBeanObjectNames.MEMORY_USAGE]
                    if isinstance(data, list):
                        for item in data:
                            if item['name'] == metric.value:
                                return item['value']
                return 0.0
        except Exception as e:
            logger.error(f"Error getting memory metric {metric.value}: {e}")
            return [] if historical else 0.0

    @staticmethod
    def build_jmx_url(hostname: str, 
                      port: int, 
                      protocol: JMXProtocol,
                      connector_name: str = "JMXRMAgent") -> str:
        """Build a JMX service URL for accessing a node."""
        if protocol == JMXProtocol.RMI:
            return f"service:jmx:rmi:///jndi/rmi://{hostname}:{port}/{connector_name}"
        elif protocol == JMXProtocol.RO:
            return f"service:jmx:ro:///jndi/pamr://{port}/{connector_name}"
        else:
            raise ValueError("Protocol must be RMI or RO (use JMXProtocol enum)")

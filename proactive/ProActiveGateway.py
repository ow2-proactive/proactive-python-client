import py4j
import os

from py4j.java_gateway import JavaGateway 


class scheduler_gateway:
    """
    Simple client for the ProActive scheduler REST API
    See also https://try.activeeon.com/rest/doc/jaxrsdocs/overview-summary.html
    """

    def __init__(self, base_url):
        """
        :param base_url: REST API base URL including host and port, for instance http://localhost:8080
        """
        
    
    
    def getStatus():
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        current_path = ROOT_DIR + "/java/lib/*"
        gg = JavaGateway.launch_gateway(classpath=os.path.normpath(current_path), die_on_exit=True )
        
        
        
        
        
        
        proactive_schduler_client = gg.jvm.org.ow2.proactive.scheduler.rest.SchedulerClient.createInstance()
        connection_info = gg.jvm.org.ow2.proactive.authentication.ConnectionInfo("https://trydev.activeeon.com/rest","bobot","proactive",None, True)
        proactive_schduler_client.init(connection_info);
        return proactive_schduler_client.getStatus().toString();

    
        
    
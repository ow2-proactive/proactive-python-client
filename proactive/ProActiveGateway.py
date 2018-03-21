import py4j
import os

from py4j.java_gateway import JavaGateway 


class scheduler_gateway:
    
    
        
    """
    Simple client for the ProActive scheduler REST API
    See also https://try.activeeon.com/rest/doc/jaxrsdocs/overview-summary.html
    """
    def __init__(self, base_url, username, password, credentials_path=None, insecure=True ):
        """
        :param base_url: REST API base URL including host and port, for instance http://localhost:8080
        """
        self.base_url = base_url
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        current_path = ROOT_DIR + "/java/lib/*"
        gg = JavaGateway.launch_gateway(classpath=os.path.normpath(current_path), die_on_exit=True )
        
        credentials_file = None
        if credentials_path is not None:
            credentials_file = gg.jvm.java.io.File(credentials_path)
             
            
        self.proactive_schduler_client = gg.jvm.org.ow2.proactive_grid_cloud_portal.smartproxy.RestSmartProxyImpl()
        connection_info = gg.jvm.org.ow2.proactive.authentication.ConnectionInfo(base_url + "/rest", username, password, credentials_file, insecure)
        self.proactive_schduler_client.init(connection_info);
    
    def submitFromCatalog(self, bucket_name, workflow_name):
        
        return self.proactive_schduler_client.submitFromCatalog(self.base_url + "/catalog",bucket_name, workflow_name).getReadableName();

    
        
    
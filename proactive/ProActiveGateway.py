import py4j
import os
from py4j.java_gateway import JavaGateway
from py4j.java_collections import MapConverter



class scheduler_gateway:
    

    """
    Simple client for the ProActive scheduler REST API
    See also https://try.activeeon.com/rest/doc/jaxrsdocs/overview-summary.html
    """
    def __init__(self, base_url,):
        """
        :param base_url: REST API base URL including host and port, for instance http://localhost:8080
        """
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        current_path = ROOT_DIR + "/java/lib/*"
        self.base_url = base_url        
        self.gateway = JavaGateway()               
        self.gg = self.gateway.launch_gateway(classpath=os.path.normpath(current_path), die_on_exit=True )
  

    def connect(self,username, password, credentials_path=None, insecure=True ):
        credentials_file = None
        if credentials_path is not None:
            credentials_file = self.gg.jvm.java.io.File(credentials_path)
            
        self.proactive_schduler_client = self.gg.jvm.org.ow2.proactive_grid_cloud_portal.smartproxy.RestSmartProxyImpl()
        connection_info = self.gg.jvm.org.ow2.proactive.authentication.ConnectionInfo(self.base_url + "/rest", username, password, credentials_file, insecure)
        self.proactive_schduler_client.init(connection_info);
        
    def disconnect(self):
        self.proactive_schduler_client.disconnect()        
    
    def submitFromCatalog(self, bucket_name, workflow_name, workflow_variables = {}):
        workflow_variables_java_map = MapConverter().convert(workflow_variables, self.gg._gateway_client)
        return self.proactive_schduler_client.submitFromCatalog(self.base_url + "/catalog",bucket_name, workflow_name, workflow_variables_java_map).longValue();

    def submitFile(self, workflow_xml_file_path, workflow_variables = {}):
        workflow_variables_java_map = MapConverter().convert(workflow_variables, self.gg._gateway_client)
        return self.proactive_schduler_client.submit(self.gg.jvm.java.io.File(workflow_xml_file_path), workflow_variables_java_map).longValue();
    
    def submitURL(self, workflow_url_spec, workflow_variables = {}):
        workflow_variables_java_map = MapConverter().convert(workflow_variables, self.gg._gateway_client)
        return self.proactive_schduler_client.submit(self.gg.jvm.java.net.URL(workflow_url_spec), workflow_variables_java_map).longValue();
    
    def getJobState(self,job_id):
        return self.proactive_schduler_client.getJobState(job_id).getName();
    
    def isJobFinished(self,job_id):
        return self.proactive_schduler_client.isJobFinished(job_id);
    
    def getJobInfo(self,job_id):
        return self.proactive_schduler_client.getJobInfo(str(job_id));
    
    def getAllJobs(self, max_number_of_jobs=1000):
        job_filter_criteria = self.gg.jvm.org.ow2.proactive.scheduler.common.JobFilterCriteria(False, False, True, False)
        jobs_page = self.proactive_schduler_client.getJobs(0, max_number_of_jobs,job_filter_criteria, None );
        return jobs_page.getList()
        


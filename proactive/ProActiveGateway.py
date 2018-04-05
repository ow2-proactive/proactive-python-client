import os

from py4j.java_gateway import JavaGateway
from py4j.java_collections import MapConverter
from .SerialisationHelper import *


class ProActiveGateway:
  """
  Simple client for the ProActive scheduler REST API
  See also https://try.activeeon.com/rest/doc/jaxrsdocs/overview-summary.html
  """
  base_url = None
  gateway = None
  runtime_gateway = None
  serialisation_helper = None
  proactive_scheduler_client = None

  def __init__(self, base_url):
    """
    :param base_url: REST API base URL including host and port, for instance http://localhost:8080
    """
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    current_path = ROOT_DIR + "/java/lib/*"
    self.base_url = base_url
    self.gateway = JavaGateway()
    self.runtime_gateway = self.gateway.launch_gateway(classpath=os.path.normpath(current_path), die_on_exit=True)
    self.serialisation_helper = SerialisationHelper(self.runtime_gateway)

  def get_runtime_gateway(self):
    return self.runtime_gateway

  def get_serialisation_helper(self):
    return self.serialisation_helper

  def connect(self, username, password, credentials_path=None, insecure=True):
    credentials_file = None
    if credentials_path is not None:
      credentials_file = self.runtime_gateway.jvm.java.io.File(credentials_path)

    self.proactive_scheduler_client = self.runtime_gateway.jvm.org.ow2.proactive_grid_cloud_portal.smartproxy.RestSmartProxyImpl()
    connection_info = self.runtime_gateway.jvm.org.ow2.proactive.authentication.ConnectionInfo(self.base_url + "/rest",
                                                                                               username, password,
                                                                                               credentials_file,
                                                                                               insecure)
    self.proactive_scheduler_client.init(connection_info)

  def disconnect(self):
    self.proactive_scheduler_client.disconnect()

  def submitWorkflowFromCatalog(self, bucket_name, workflow_name, workflow_variables={}):
    workflow_variables_java_map = MapConverter().convert(workflow_variables, self.runtime_gateway._gateway_client)
    return self.proactive_scheduler_client.submitFromCatalog(self.base_url + "/catalog", bucket_name, workflow_name,
                                                             workflow_variables_java_map).longValue()

  def submitWorkflowFromFile(self, workflow_xml_file_path, workflow_variables={}):
    workflow_variables_java_map = MapConverter().convert(workflow_variables, self.runtime_gateway._gateway_client)
    return self.proactive_scheduler_client.submit(self.runtime_gateway.jvm.java.io.File(workflow_xml_file_path),
                                                  workflow_variables_java_map).longValue()

  def submitWorkflowFromURL(self, workflow_url_spec, workflow_variables={}):
    workflow_variables_java_map = MapConverter().convert(workflow_variables, self.runtime_gateway._gateway_client)
    return self.proactive_scheduler_client.submit(self.runtime_gateway.jvm.java.net.URL(workflow_url_spec),
                                                  workflow_variables_java_map).longValue()

  def submitPythonLambda(self, l, python_path=None):
    job = self.serialisation_helper.create_python_task_from_function(l, python_path)
    return self.proactive_scheduler_client.submit(job).longValue()

  def submitPythonTask(self, script_python, script_params = {}):
    job = self.serialisation_helper.create_python_task_from_script(script_python, script_params)
    return self.proactive_scheduler_client.submit(job).longValue()

  def submitPythonTaskFromFile(self, file_python, script_params = {}):
    job = self.serialisation_helper.create_python_task_from_file(file_python, script_params)
    return self.proactive_scheduler_client.submit(job).longValue()

  def getJobState(self, job_id):
    return self.proactive_scheduler_client.getJobState(job_id).getName()

  def isJobFinished(self, job_id):
    return self.proactive_scheduler_client.isJobFinished(job_id)

  def getJobInfo(self, job_id):
    return self.proactive_scheduler_client.getJobInfo(str(job_id))

  def getAllJobs(self, max_number_of_jobs=1000):
    job_filter_criteria = self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.JobFilterCriteria(False, False,
                                                                                                        True, False)
    jobs_page = self.proactive_scheduler_client.getJobs(0, max_number_of_jobs, job_filter_criteria, None)
    return jobs_page.getList()


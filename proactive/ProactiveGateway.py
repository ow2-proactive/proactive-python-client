import os
import sys

from py4j.java_gateway import JavaGateway
from py4j.java_collections import MapConverter

from .ProactiveFactory import *
from .ProactiveBuilder import *

from .model.ProactiveScriptLanguage import *
from .model.ProactiveSelectionScript import *
from .model.ProactiveForkEnv import *
from .model.ProactiveTask import *
from .model.ProactiveJob import *


class ProActiveGateway:
  """
  Simple client for the ProActive scheduler REST API
  See also https://try.activeeon.com/rest/doc/jaxrsdocs/overview-summary.html
  """
  root_dir = ''
  current_path = ''
  base_url = None
  gateway = None
  runtime_gateway = None
  proactive_scheduler_client = None
  proactive_factory = None

  def __init__(self, base_url, javaopts=[], redirectJVMOutput=False):
    self.root_dir = os.path.dirname(os.path.abspath(__file__))
    self.current_path = self.root_dir + "/java/lib/*"
    self.base_url = base_url
    self.gateway = JavaGateway()
    self.javaopts = javaopts
    #self.javaopts.append('-Dlog4j.configuration=file:'+os.path.join(os.getcwd(),'log4j.properties'))
    self.redirect_stdout = None
    self.redirect_stderr = None

    if redirectJVMOutput:
      self.redirect_stdout = sys.stdout
      self.redirect_stderr = sys.stderr

    self.runtime_gateway = self.gateway.launch_gateway(
      classpath=os.path.normpath(self.current_path),
      die_on_exit=True,
      javaopts=self.javaopts,
      redirect_stdout=self.redirect_stdout,
      redirect_stderr=self.redirect_stderr,
    )
    self.proactive_factory = ProactiveFactory(self.runtime_gateway)

  def connect(self, username, password, credentials_path=None, insecure=True):
    credentials_file = None
    if credentials_path is not None:
      credentials_file = self.runtime_gateway.jvm.java.io.File(credentials_path)

    self.proactive_scheduler_client = self.proactive_factory.create_smart_proxy()
    connection_info = self.proactive_factory.create_connection_info(
      self.base_url + "/rest", username, password, credentials_file, insecure
    )
    self.proactive_scheduler_client.init(connection_info)

  def isConnected(self):
    return self.proactive_scheduler_client.isConnected()

  def disconnect(self):
    self.proactive_scheduler_client.disconnect()

  def reconnect(self):
    self.proactive_scheduler_client.reconnect()

  def terminate(self):
    self.proactive_scheduler_client.terminate()

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

  def createTask(self, language=None):
    return ProactiveTask(language)

  def createPythonTask(self):
    return ProactiveTask(self.getProactiveScriptLanguage().python())

  def createJob(self):
    return ProactiveJob()

  def submitJob(self, job_model, debug=False):
    proactive_job = ProactiveJobBuilder(self.proactive_factory, job_model).create().display(debug).getProactiveJob()
    user_space_uri = self.proactive_scheduler_client.getUserSpaceURIs()[0]
    proactive_job.setInputSpace(user_space_uri)
    proactive_job.setOutputSpace(user_space_uri)
    return self.proactive_scheduler_client.submit(
      proactive_job,
      job_model.getInputFolder(),
      job_model.getOutputFolder(),
      False,
      True
    ).longValue()

  def createForkEnvironment(self, language=None):
    return ProactiveForkEnv(language)

  def createDefaultForkEnvironment(self):
    return ProactiveForkEnv(self.getProactiveScriptLanguage().jython())

  def createPythonForkEnvironment(self):
    return ProactiveForkEnv(self.getProactiveScriptLanguage().python())

  def createSelectionScript(self, language=None):
    return ProactiveSelectionScript(language)

  def createDefaultSelectionScript(self):
    return ProactiveSelectionScript(self.getProactiveScriptLanguage().jython())

  def createPythonSelectionScript(self):
    return ProactiveSelectionScript(self.getProactiveScriptLanguage().python())

  def getProactiveScriptLanguage(self):
      return ProactiveScriptLanguage()

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

  def getJobResult(self, job_id, timeout=60000):
    job_result = self.proactive_scheduler_client.waitForJob(str(job_id), timeout)
    all_results = []
    for result in job_result.getAllResults().values():
      if type(result.getValue()) is bytes:
        all_results.append(result.getValue().decode('ascii'))
      else:
        all_results.append(str(result.getValue()))
    return '\n'.join(v for v in all_results)

  def getTaskResult(self, job_id, task_name, timeout=60000):
    job_result = self.proactive_scheduler_client.waitForJob(str(job_id), timeout)
    return job_result.getAllResults().get(task_name).getValue()


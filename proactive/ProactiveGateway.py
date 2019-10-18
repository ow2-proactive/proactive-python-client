import os
import sys

from py4j.java_gateway import JavaGateway
from py4j.java_collections import MapConverter

from .ProactiveFactory import *
from .ProactiveBuilder import *

from .model.ProactiveScript import *
from .model.ProactiveScriptLanguage import *
from .model.ProactiveSelectionScript import *
from .model.ProactiveForkEnv import *
from .model.ProactiveFlowScript import *
from .model.ProactiveFlowBlock import *
from .model.ProactiveFlowActionType import *
from .model.ProactiveTask import *
from .model.ProactiveJob import *

class ProActiveGateway:
    """
    Simple client for the ProActive scheduler REST API
    See also https://try.activeeon.com/rest/doc/jaxrsdocs/overview-summary.html
    """

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
        self.proactive_script_language = ProactiveScriptLanguage()
        self.proactive_flow_block = ProactiveFlowBlock()
        self.proactive_flow_action_type = ProactiveFlowActionType()

        self.proactive_scheduler_client = self.proactive_factory.create_smart_proxy()

    def connect(self, username, password, credentials_path=None, insecure=True):
        credentials_file = None
        if credentials_path is not None:
            credentials_file = self.runtime_gateway.jvm.java.io.File(credentials_path)

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
        return ProactiveTask(language) if self.proactive_script_language.is_language_supported(language) else None

    def createPythonTask(self):
        return ProactivePythonTask()

    def createFlowScript(self, script_language=None):
        if script_language is None:
            script_language = self.proactive_script_language.javascript()
        return ProactiveFlowScript(script_language)

    def createReplicateFlowScript(self, script_implementation, script_language="javascript"):
        flow_script = ProactiveFlowScript(script_language)
        flow_script.setActionType(self.proactive_flow_action_type.replicate())
        flow_script.setImplementation(script_implementation)
        return flow_script

    def createLoopFlowScript(self, script_implementation, target, script_language="javascript"):
        flow_script = ProactiveFlowScript(script_language)
        flow_script.setActionType(self.proactive_flow_action_type.loop())
        flow_script.setImplementation(script_implementation)
        flow_script.setActionTarget(target)
        return flow_script

    def createBranchFlowScript(self, script_implementation, target_if, target_else, target_continuation,
                               script_language="javascript"):
        flow_script = ProactiveFlowScript(script_language)
        flow_script.setActionType(self.proactive_flow_action_type.branch())
        flow_script.setImplementation(script_implementation)
        flow_script.setActionTarget(target_if)
        flow_script.setActionTargetElse(target_else)
        flow_script.setActionTargetContinuation(target_continuation)
        return flow_script

    def getProactiveFlowBlockType(self):
        return self.proactive_flow_block

    def createPreScript(self, language=None):
        return ProactivePreScript(language) if self.proactive_script_language.is_language_supported(language) else None

    def createPostScript(self, language=None):
        return ProactivePostScript(language) if self.proactive_script_language.is_language_supported(language) else None

    def createJob(self):
        return ProactiveJob()

    def buildJob(self, job_model, debug=False):
        return ProactiveJobBuilder(self.proactive_factory, job_model).create().display(debug).getProactiveJob()

    def submitJob(self, job_model, debug=False):
        proactive_job = self.buildJob(job_model, debug)
        return self.proactive_scheduler_client.submit(
            proactive_job,
            job_model.getInputFolder(),
            job_model.getOutputFolder(),
            False,
            True
        ).longValue()

    def createForkEnvironment(self, language=None):
        return ProactiveForkEnv(language) if self.proactive_script_language.is_language_supported(language) else None

    def createDefaultForkEnvironment(self):
        return ProactiveForkEnv(self.proactive_script_language.jython())

    def createPythonForkEnvironment(self):
        return ProactiveForkEnv(self.proactive_script_language.python())

    def createSelectionScript(self, language=None):
        return ProactiveSelectionScript(language) if self.proactive_script_language.is_language_supported(language) else None

    def createDefaultSelectionScript(self):
        return ProactiveSelectionScript(self.proactive_script_language.jython())

    def createPythonSelectionScript(self):
        return ProactiveSelectionScript(self.proactive_script_language.python())

    def getProactiveClient(self):
        return self.proactive_scheduler_client

    def getProactiveScriptLanguage(self):
        return self.proactive_script_language

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

    @staticmethod
    def __decode__(value):
        return value.decode('ascii')

    def getJobResult(self, job_id, timeout=60000):
        job_result = self.proactive_scheduler_client.waitForJob(str(job_id), timeout)
        all_results = []
        for result in job_result.getAllResults().values():
            if type(result.getValue()) is bytes:
                all_results.append(self.__decode__(result.getValue()))
            else:
                all_results.append(str(result.getValue()))
        return os.linesep.join(v for v in all_results)

    def getTaskResult(self, job_id, task_name, timeout=60000):
        task_result = self.proactive_scheduler_client.waitForTask(str(job_id), task_name, timeout)
        if type(task_result.getValue()) is bytes:
            task_result = self.__decode__(task_result.getValue())
        return task_result.getValue()

    def printJobOutput(self, job_id, timeout=60000):
        job_result = self.proactive_scheduler_client.waitForJob(str(job_id), timeout)
        all_outputs = []
        for result in job_result.getAllResults().values():
            all_outputs.append(result.getOutput().getStdoutLogs().strip(' \n'))
        return os.linesep.join(v for v in all_outputs)

    def printTaskOutput(self, job_id, task_name, timeout=60000):
        task_output = self.proactive_scheduler_client.waitForTask(str(job_id), task_name, timeout).getOutput()
        return task_output.getStdoutLogs().strip(' \n')

    def exportJob2XML(self, job_model, debug=False):
        proactive_job = self.buildJob(job_model, debug)
        Job2XMLTransformer = self.proactive_factory.create_job2xml_transformer()
        return Job2XMLTransformer.jobToxmlString(proactive_job)

    def saveJob2XML(self, job_model, xml_file_path, debug=False):
        job_xml_data = self.exportJob2XML(job_model, debug)
        with open(xml_file_path, "w") as text_file:
            text_file.write("{0}".format(job_xml_data))


import sys
import getpass

from py4j.java_gateway import JavaGateway

import logging.config

from .ProactiveRestApi import *
from .ProactiveFactory import *
from .ProactiveBuilder import *

from .model.ProactiveForkEnv import *
from .model.ProactiveFlowScript import *
from .model.ProactiveFlowBlock import *
from .model.ProactiveFlowActionType import *
from .model.ProactiveTask import *
from .model.ProactiveJob import *


class ProActiveGateway:
    """
    Simple client for the ProActive scheduler REST API
    See also https://try.activeeon.com/doc/rest/
    """

    def __init__(self, base_url, debug=False, javaopts=[], log4j_props_file=None, log4py_props_file=None):
        """
        Create a Proactive Gateway

        :param base_url: The Proactive server base URL
        :param debug: If set True, the gateway will be created with the debug mode
        :param javaopts: Some additional java options
        :param log4j_props_file: The log4j properties file path
        :param log4py_props_file: The log4py properties file path
        """
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.current_path = self.root_dir + "/java/lib/*"
        self.base_url = base_url
        self.gateway = JavaGateway()
        self.proactive_rest_api = ProactiveRestApi()
        self.javaopts = javaopts
        self.redirect_stdout = None
        self.redirect_stderr = None
        self.debug = debug
        self.log4py_props_file = log4py_props_file

        if self.debug:
            if log4j_props_file:
                self.log4j_props_file = log4j_props_file
            else:
                self.log4j_props_file = os.path.join(self.root_dir + "/java", 'log4j.properties')
            if self.log4py_props_file is None:
                self.log4py_props_file = os.path.join(self.root_dir, 'logging.conf')
            self.javaopts.append('-Dlog4j.configuration=file:' + self.log4j_props_file)
            self.redirect_stdout = sys.stdout
            self.redirect_stderr = sys.stderr
            logging.config.fileConfig(self.log4py_props_file)

        self.logger = logging.getLogger('ProactiveGateway')
        self.logger.debug('Launching JVM gateway with javaopts = ' + str(self.javaopts))

        try:
            self.runtime_gateway = self.gateway.launch_gateway(
                classpath=os.path.normpath(self.current_path),
                die_on_exit=True,
                javaopts=self.javaopts,
                redirect_stdout=self.redirect_stdout,
                redirect_stderr=self.redirect_stderr,
            )
        except Exception:
            self.runtime_gateway = self.gateway.launch_gateway(
                classpath=os.path.normpath(self.current_path),
                die_on_exit=True,
                javaopts=self.javaopts,
                redirect_stdout=None,
                redirect_stderr=None,
            )

        self.logger.debug('JVM gateway launched with success')
        self.proactive_factory = ProactiveFactory(self.runtime_gateway)
        self.proactive_script_language = ProactiveScriptLanguage()
        self.proactive_flow_block = ProactiveFlowBlock()
        self.proactive_flow_action_type = ProactiveFlowActionType()

        self.proactive_scheduler_client = self.proactive_factory.create_smart_proxy()

    def connect(self, username=None, password=None, credentials_path=None, insecure=True):
        """
        Connect to a Proactive server

        :param username: A valid username
        :param password: A valid password
        :param credentials_path: A credentials file path
        :param insecure: If set True, the gateway will connect in insecure mode
        """
        credentials_file = None
        if credentials_path is not None:
            credentials_file = self.runtime_gateway.jvm.java.io.File(credentials_path)

        if username is None:
            username = input('Login: ')

        if password is None:
            password = getpass.getpass(prompt='Password: ')

        connection_info = self.proactive_factory.create_connection_info(
            self.base_url + "/rest", username, password, credentials_file, insecure
        )
        self.logger.debug('Connecting to the ProActive server')
        self.proactive_scheduler_client.init(connection_info)
        self.proactive_rest_api.init(connection_info)
        self.logger.debug('Connected on ' + self.base_url)

    def isConnected(self):
        """
        Verify if the gateway is connected to the ProActive server

        :return: True or False
        """
        return self.proactive_scheduler_client.isConnected()

    def disconnect(self):
        """
        Disconnect the gateway from the ProActive server
        """
        self.logger.debug('Disconnecting from the ProActive server')
        self.proactive_scheduler_client.disconnect()
        self.proactive_rest_api.disconnect()
        self.logger.debug('Disconnected.')

    def reconnect(self):
        """
        Reconnect the gateway to the ProActive server
        """
        self.logger.debug('Reconnecting to the ProActive server')
        self.proactive_scheduler_client.reconnect()
        self.proactive_rest_api.reconnect()
        self.logger.debug('Reconnected')

    def terminate(self):
        """
        Terminate the connection
        """
        self.proactive_rest_api.disconnect()
        self.proactive_scheduler_client.terminate()
        self.runtime_gateway.close()
        self.runtime_gateway.shutdown()
        self.runtime_gateway.java_process.stdin.write("\n".encode("utf-8"))
        self.runtime_gateway.java_process.stdin.flush()
        self.runtime_gateway.java_process.wait(1)
        del self.proactive_scheduler_client
        del self.runtime_gateway

    def getProactiveRestApi(self):
        return self.proactive_rest_api

    def getRuntimeGateway(self):
        return self.runtime_gateway

    def submitWorkflowFromCatalog(self, bucket_name, workflow_name, workflow_variables={}, workflow_generic_info={}):
        """
        Submit a job from the catalog to the scheduler

        :param bucket_name: The bucket in which the workflow is saved
        :param workflow_name: The workflow name
        :param workflow_variables: The workflow input variables
        :param workflow_generic_info: The workflow generic information
        :return: The submitted job id
        """
        workflow_variables_java_map = MapConverter().convert(workflow_variables, self.runtime_gateway._gateway_client)
        workflow_generic_info_java_map = MapConverter().convert(workflow_generic_info, self.runtime_gateway._gateway_client)
        self.logger.debug('Submitting from catalog the job \'' + bucket_name + '/' + workflow_name + '\'')
        return self.proactive_scheduler_client.submitFromCatalog(self.base_url + "/catalog", bucket_name, workflow_name,
                                                                 workflow_variables_java_map, workflow_generic_info_java_map).longValue()

    def submitWorkflowFromFile(self, workflow_xml_file_path, workflow_variables={}):
        """
        Submit a job from an xml file to the scheduler

        :param workflow_xml_file_path: The workflow xml file path
        :param workflow_variables: The workflow input variables
        :return: The submitted job id
        """
        workflow_variables_java_map = MapConverter().convert(workflow_variables, self.runtime_gateway._gateway_client)
        self.logger.debug('Submitting from file the job \'' + workflow_xml_file_path + '\'')
        return self.proactive_scheduler_client.submit(self.runtime_gateway.jvm.java.io.File(workflow_xml_file_path),
                                                      workflow_variables_java_map).longValue()

    def submitWorkflowFromURL(self, workflow_url_spec, workflow_variables={}):
        """
        Submit a job from an url to the scheduler

        :param workflow_url_spec: The workflow url
        :param workflow_variables: The workflow input variables
        :return: The submitted job id
        """
        workflow_variables_java_map = MapConverter().convert(workflow_variables, self.runtime_gateway._gateway_client)
        self.logger.debug('Submitting from URL the job \'' + workflow_url_spec + '\'')
        return self.proactive_scheduler_client.submit(self.runtime_gateway.jvm.java.net.URL(workflow_url_spec),
                                                      workflow_variables_java_map).longValue()

    def createTask(self, language=None):
        """
        Create a workflow task

        :param language: The script language
        :return: A ProactiveTask object
        """
        self.logger.info('Creating a task')
        return ProactiveTask(language) if self.proactive_script_language.is_language_supported(language) else None

    def createPythonTask(self):
        """
        Create a workflow Python task

        :return: A Python ProactiveTask object
        """
        self.logger.info('Creating a Python task')
        return ProactivePythonTask()

    def createFlowScript(self, script_language=None):
        """
        Create a flow script

        :param script_language: The script language
        :return: A ProactiveFlowScript object
        """
        if script_language is None:
            script_language = self.proactive_script_language.javascript()
        self.logger.info('Creating a flow script')
        return ProactiveFlowScript(script_language)

    def createReplicateFlowScript(self, script_implementation, script_language="javascript"):
        """
        Create a replicate flow script

        :param script_implementation: The script implementation
        :param script_language: The script language
        :return: A replicate ProactiveFlowScript object
        """
        self.logger.info('Creating a Replicate flow script')
        flow_script = ProactiveFlowScript(script_language)
        flow_script.setActionType(self.proactive_flow_action_type.replicate())
        flow_script.setImplementation(script_implementation)
        return flow_script

    def createLoopFlowScript(self, script_implementation, target, script_language="javascript"):
        """
        Create a loop flow script

        :param script_implementation: The script implementation
        :param target: The loop target
        :param script_language: The script language
        :return: A loop ProactiveFlowScript object
        """
        self.logger.info('Creating a Loop flow script')
        flow_script = ProactiveFlowScript(script_language)
        flow_script.setActionType(self.proactive_flow_action_type.loop())
        flow_script.setImplementation(script_implementation)
        flow_script.setActionTarget(target)
        return flow_script

    def createBranchFlowScript(self, script_implementation, target_if, target_else, target_continuation,
                               script_language="javascript"):
        """
        Create a branch flow script

        :param script_implementation: The script implementation
        :param target_if: The if target task
        :param target_else: The else target task
        :param target_continuation: The continuationn target task
        :param script_language: The script language
        :return: A branch ProactiveFlowScript object
        """
        self.logger.info('Creating a Branch flow script')
        flow_script = ProactiveFlowScript(script_language)
        flow_script.setActionType(self.proactive_flow_action_type.branch())
        flow_script.setImplementation(script_implementation)
        flow_script.setActionTarget(target_if)
        flow_script.setActionTargetElse(target_else)
        flow_script.setActionTargetContinuation(target_continuation)
        return flow_script

    def getProactiveFlowBlockType(self):
        """
        Get the Proactive flow block

        :return: The ProactiveFlowBlock object
        """
        return self.proactive_flow_block

    def createPreScript(self, language=None):
        """
        Create a Proactive pre-script

        :param language: The script language
        :return: A ProactivePreScript object
        """
        self.logger.info('Creating a pre script')
        return ProactivePreScript(language) if self.proactive_script_language.is_language_supported(language) else None

    def createPostScript(self, language=None):
        """
        Create a Proactive post-script

        :param language: The script language
        :return: A ProactivePostScript object
        """
        self.logger.info('Creating a post script')
        return ProactivePostScript(language) if self.proactive_script_language.is_language_supported(language) else None

    def createJob(self):
        """
        Create a Proactive Job

        :return: A ProactiveJob object
        """
        self.logger.info('Creating a job')
        return ProactiveJob()

    def buildJob(self, job_model, debug=False):
        """
        Build the Proactive job to be submitted to the scheduler

        :param job_model: A valid job model
        :param debug: If set True, the submitted job will be printed for a debugging purpose
        :return: A Proactive job ready to be submitted
        """
        self.logger.info('Building the job' + job_model.getJobName())
        return ProactiveJobBuilder(self.proactive_factory, job_model, self.debug, self.log4py_props_file).create().display(debug).getProactiveJob()

    def submitJob(self, job_model, debug=False):
        """
        Submit a job to the Proactive Scheduler

        :param job_model: A valid job model
        :param debug: If set True, the submitted job will be printed for a debugging purpose
        :return: The submitted job ID
        """
        proactive_job = self.buildJob(job_model, debug)
        self.logger.info('Submitting the job' + job_model.getJobName())
        return self.proactive_scheduler_client.submit(proactive_job).longValue()

    def submitJobWithInputsAndOutputsPaths(self, job_model, input_folder_path='.', output_folder_path='.', debug=False):
        """
        Submit a job to the Proactive Scheduler with input and output paths

        :param job_model: A valid job model
        :param input_folder_path: Path to the directory containing input files
        :param output_folder_path: Path to the local directory which will contain output files
        :param debug: If set True, the submitted job will be printed for a debugging purpose
        :return: The submitted job ID
        """
        proactive_job = self.buildJob(job_model, debug)
        self.logger.info('Submitting the job' + job_model.getJobName())
        return self.proactive_scheduler_client.submit(
            proactive_job,
            input_folder_path,
            output_folder_path,
            False,
            True
        ).longValue()

    def createForkEnvironment(self, language=None):
        """
        Create a Proactive fork environment

        :param language: The script language
        :return: A ProactiveForkEnv object
        """
        self.logger.info('Creating a fork environment')
        return ProactiveForkEnv(language) if self.proactive_script_language.is_language_supported(language) else None

    def createDefaultForkEnvironment(self):
        """
        Create a default fork environment

        :return: A default ProactiveForkEnv object
        """
        self.logger.info('Creating a default fork environment')
        return ProactiveForkEnv(self.proactive_script_language.jython())

    def createPythonForkEnvironment(self):
        """
        Create a Python fork environment

        :return: A Python ProactiveForkEnv object
        """
        self.logger.info('Creating a Python fork environment')
        return ProactiveForkEnv(self.proactive_script_language.python())

    def createSelectionScript(self, language=None):
        """
        Create a Proactive selection script

        :param language: The script language
        :return: A ProactiveSelectionScript object
        """
        self.logger.info('Creating a selection script')
        return ProactiveSelectionScript(language) if self.proactive_script_language.is_language_supported(language) else None

    def createDefaultSelectionScript(self):
        """
        Create a default selection script

        :return: A default ProactiveSelectionScript object
        """
        self.logger.info('Creating a default selection script')
        return ProactiveSelectionScript(self.proactive_script_language.jython())

    def createPythonSelectionScript(self):
        """
        Create a Python selection script

        :return: A Python ProactiveSelectionScript object
        """
        self.logger.info('Creating a Python selection script')
        return ProactiveSelectionScript(self.proactive_script_language.python())

    def getProactiveClient(self):
        """
        Get the Proactive gateway

        :return: A smart proxy object
        """
        return self.proactive_scheduler_client

    def getProactiveScriptLanguage(self):
        """
        Get Proactive script languages

        :return: The ProactiveScriptLanguage object
        """
        return self.proactive_script_language

    def getJobState(self, job_id):
        """
        Get the job state

        :param job_id: A valid job ID
        :return: The job state
        """
        return self.proactive_scheduler_client.getJobState(job_id).getName()

    def isJobFinished(self, job_id):
        """
        Verify if a job is finished

        :param job_id: A valid job ID
        :return: True or False
        """
        return self.proactive_scheduler_client.isJobFinished(job_id)

    def getJobInfo(self, job_id):
        """
        Get the job info

        :param job_id: A valid job ID
        :return: The job info
        """
        return self.proactive_scheduler_client.getJobInfo(str(job_id))

    def getAllJobs(self, max_number_of_jobs=1000, my_jobs_only=False, pending=False, running=True, finished=False,
                   withIssuesOnly=False, child_jobs=True, job_name=None, project_name=None, user_name=None, tenant=None, parent_id=None):
        """
        Get all jobs from the ProActive scheduler

        :param my_jobs_only: Get only my jobs
        :param pending: Include jobs in PENDING state
        :param running: Include jobs in RUNNING state
        :param finished: Include jobs in FINISHED state
        :param withIssuesOnly: Include only jobs with issues
        :param child_jobs: Include child jobs
        :param job_name: Get jobs with specific job name
        :param project_name: Get jobs with specific project name
        :param user_name: Get jobs of specific user
        :param tenant: Get jobs having specific tenant
        :param parent_id: Get jobs related to a specific parent job id
        :param max_number_of_jobs: The maximal number of retrieved jobs
        :return: A list of jobs
        """
        job_filter_criteria = self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.JobFilterCriteriaBuilder().myJobsOnly(my_jobs_only).pending(pending).running(running).finished(finished).withIssuesOnly(withIssuesOnly).childJobs(child_jobs).jobName(job_name).projectName(project_name).userName(user_name).tenant(tenant).parentId(parent_id).build()
        jobs_page = self.proactive_scheduler_client.getJobs(0, max_number_of_jobs, job_filter_criteria, None)
        return jobs_page.getList()

    @staticmethod
    def __decode__(value):
        return value.decode('ascii')

    def getJobResult(self, job_id, timeout=60000):
        """
        Get the job result

        :param job_id: A valid job ID
        :param timeout: A timeout in milliseconds
        :return: The job results
        """
        self.logger.debug('Getting job\'s results')
        job_result = self.proactive_scheduler_client.waitForJob(str(job_id), timeout)
        all_results = []
        self.logger.debug('Formatting results')
        for result in job_result.getAllResults().values():
            if type(result.getValue()) is bytes:
                all_results.append(self.__decode__(result.getValue()))
            else:
                all_results.append(str(result.getValue()))
        return os.linesep.join(v for v in all_results)

    def getTaskResult(self, job_id, task_name, timeout=60000):
        """
        Get the task result

        :param job_id: A valid job ID
        :param task_name: A valid task name
        :param timeout: A timeout in milliseconds
        :return: The task results
        """
        self.logger.debug('Getting results of the task \'' + task_name + '\'')
        task_result = self.proactive_scheduler_client.waitForTask(str(job_id), task_name, timeout)
        self.logger.debug('Formatting results')
        if type(task_result.getValue()) is bytes:
            task_result = self.__decode__(task_result.getValue())
        return task_result.getValue()

    def printJobOutput(self, job_id, timeout=60000):
        """
        Get the job output

        :param job_id: A valid job ID
        :param timeout: A timeout in milliseconds
        :return: The job outputs
        """
        self.logger.debug('Getting job\'s outputs')
        job_result = self.proactive_scheduler_client.waitForJob(str(job_id), timeout)
        all_outputs = []
        self.logger.debug('Formatting outputs')
        for result in job_result.getAllResults().values():
            all_outputs.append(result.getOutput().getStdoutLogs().strip(' \n'))
        return os.linesep.join(v for v in all_outputs)

    def printTaskOutput(self, job_id, task_name, timeout=60000):
        """
        Get the task outputs

        :param job_id: A valid job ID
        :param task_name: A valid task name
        :param timeout: A timeout in milliseconds
        :return: The task outputs
        """
        self.logger.debug('Getting the task \'' + task_name + '\'\'s outputs')
        task_output = self.proactive_scheduler_client.waitForTask(str(job_id), task_name, timeout).getOutput()
        return task_output.getStdoutLogs().strip(' \n')

    def exportJob2XML(self, job_model, debug=False):
        """
        Export the job to an XML file

        :param job_model: A valid job model
        :param debug: If set True, the created job will be printed for a debugging purpose
        :return: The created job as an XML script
        """
        proactive_job = self.buildJob(job_model, debug)
        self.logger.info('Transforming the job \'' + job_model.getJobName() + '\' to an XML string')
        Job2XMLTransformer = self.proactive_factory.create_job2xml_transformer()
        return Job2XMLTransformer.jobToxmlString(proactive_job)

    def saveJob2XML(self, job_model, xml_file_path, debug=False):
        """
        Save a job to an external XML file

        :param job_model: A valid job model
        :param xml_file_path: A valid XML file path
        :param debug: If set True, the created job will be printed for a debugging purpose
        """
        self.logger.info('Saving the job \'' + job_model.getJobName() + '\' to the XML file \'' + xml_file_path + '\'')
        job_xml_data = self.exportJob2XML(job_model, debug)
        with open(xml_file_path, "w") as text_file:
            text_file.write("{0}".format(job_xml_data))

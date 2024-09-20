import os
import sys
import getpass
import time
import tempfile

from py4j.java_gateway import JavaGateway
from py4j.java_collections import MapConverter, SetConverter

import logging
# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ProactiveGateway')

from .ProactiveRestApi import *
from .ProactiveFactory import *
from .ProactiveBuilder import *

from .model.ProactiveForkEnv import *
from .model.ProactiveFlowScript import *
from .model.ProactiveFlowBlock import *
from .model.ProactiveFlowActionType import *
from .model.ProactiveTask import *
from .model.ProactiveJob import *

from .bucket.ProactiveBucketFactory import *

def convert_java_map_to_python_dict(java_map):
    return {entry.getKey(): entry.getValue() for entry in java_map.entrySet()}

class ProActiveGateway:
    """
    This class provides a client for interacting with the ProActive scheduler and resource manager.
    It offers methods to create and manage jobs and tasks, handle data transfers, and execute workflows.

    Simple client for the ProActive scheduler REST API
    See also https://try.activeeon.com/doc/rest/
    """

    def __init__(self, base_url, debug=False, javaopts=[], log4j_props_file=None, log4py_props_file=None):
        """
        Initializes a new instance of the ProActiveGateway class.

        :param base_url: The base URL of the ProActive server.
        :param debug: If True, enables debug mode which provides additional logging information.
        :param javaopts: A list of additional options to pass to the Java virtual machine.
        :param log4j_props_file: The path to the log4j properties file for configuring logging.
        :param log4py_props_file: The path to the log4py properties file for configuring logging.
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
        Connects to the ProActive server using either provided credentials or a credentials file.

        :param username: The username for authentication.
        :param password: The password for authentication.
        :param credentials_path: The path to a credentials file.
        :param insecure: If True, connects without verifying the SSL certificate. Use with caution.
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
        Checks if the gateway is currently connected to the ProActive server.

        :return: True if connected, False otherwise.
        """
        return self.proactive_scheduler_client.isConnected()

    def disconnect(self):
        """
        Disconnects the gateway from the ProActive server and cleans up resources.
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
        Terminates the connection to the ProActive server and cleans up resources.
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

    def close(self):
        """
        A convenience method for disconnecting and then terminating the gateway.
        """
        self.disconnect()
        self.terminate()

    def getProactiveRestApi(self):
        return self.proactive_rest_api

    def getRuntimeGateway(self):
        return self.runtime_gateway

    def getBucket(self, bucket_name):
        self.logger.debug('Returning the bucket: ' + bucket_name)
        return ProactiveBucketFactory().getBucket(self, bucket_name)

    def submitWorkflowFromCatalog(self, bucket_name, workflow_name, workflow_variables={}, workflow_generic_info={}):
        """
        Submits a job from the ProActive catalog to the scheduler.

        :param bucket_name: The name of the bucket containing the workflow.
        :param workflow_name: The name of the workflow to be submitted.
        :param workflow_variables: A dictionary of variables to be passed to the workflow.
        :param workflow_generic_info: A dictionary of generic information to be associated with the job.
        :return: The ID of the submitted job.
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

    def submitCustomWorkflowFromFile(self, workflow_xml_file_path, workflow_variables=None, workflow_generic_info=None, job_name=None, job_description=None, project_name=None, bucket_name=None, label=None, workflow_tags=None):
        self.logger.info('Creating a proactive job from the XML file \'' + workflow_xml_file_path + '\'')
        StaxJobFactory = self.proactive_factory.create_stax_job_factory()
        Job = StaxJobFactory.createJob(workflow_xml_file_path)
        if job_name:
            Job.setName(job_name)
        if job_description:
            Job.setDescription(job_description)
        if project_name:
            Job.setProjectName(project_name)
        if bucket_name:
            Job.setBucketName(bucket_name)
        if label:
            Job.setLabel(label)
        if isinstance(workflow_variables, dict):
            self.logger.debug('Adding variables')
            job_variables = {}
            for key, value in workflow_variables.items():
                JobVariable = self.proactive_factory.create_job_variable()
                JobVariable.setName(key)
                JobVariable.setValue(value)
                job_variables[key] = JobVariable
            variables_java_map = MapConverter().convert(job_variables, self.runtime_gateway._gateway_client)
            current_variables_java_map = Job.getVariables()
            current_variables_python_dict = convert_java_map_to_python_dict(current_variables_java_map)
            new_variables_python_dict = convert_java_map_to_python_dict(variables_java_map)
            merged_variables_python_dict = {**current_variables_python_dict, **new_variables_python_dict}
            merged_variables_java_map = MapConverter().convert(merged_variables_python_dict, self.runtime_gateway._gateway_client)
            Job.setVariables(merged_variables_java_map)
        if isinstance(workflow_generic_info, dict):
            self.logger.debug('Adding the generic information')
            for key, value in workflow_generic_info.items():
                Job.addGenericInformation(key, value)
        if isinstance(workflow_tags, list):
            self.logger.debug('Adding tags')
            workflow_tags_java_set = SetConverter().convert(workflow_tags, self.runtime_gateway._gateway_client)
            Job.setWorkflowTags(workflow_tags_java_set)
        self.logger.info('Submitting the job ' + Job.getName())
        return self.proactive_scheduler_client.submit(Job).longValue()

    def submitCustomWorkflowFromCatalog(self, bucket_name, workflow_name, workflow_variables=None, workflow_generic_info=None, job_name=None, job_description=None, project_name=None, workflow_tags=None, local_file_path=None):
        try:
            object_str = self.getProactiveRestApi().get_object_from_catalog(bucket_name, workflow_name)
            PA_CATALOG_REST_URL = self.base_url + "/catalog"
            self.logger.debug("PA_CATALOG_REST_URL: " + PA_CATALOG_REST_URL)
            object_str = object_str.replace('${PA_CATALOG_REST_URL}', PA_CATALOG_REST_URL)
            # Create a temporary file that will be deleted automatically
            with tempfile.NamedTemporaryFile() as temp_file:
                # Write some data to the file
                temp_file.write(object_str.encode('utf-8'))
                # Get the absolute path of the temporary file
                temp_file_path = os.path.abspath(temp_file.name)
                # The file will be deleted when closed
                self.logger.info('Temporary file created and will be deleted: {}'.format(temp_file_path))
                # Copy the content to a new file
                if local_file_path:
                    # local_copy_path = os.path.join(os.getcwd(), 'workflow.xml')
                    with open(local_file_path, 'wb') as local_copy_file:
                        temp_file.seek(0)
                        local_copy_file.write(temp_file.read())
                    self.logger.info('Local copy of the temporary file created: {}'.format(local_file_path))
                StaxJobFactory = self.proactive_factory.create_stax_job_factory()
                Job = StaxJobFactory.createJob(temp_file_path)
                if job_name:
                    Job.setName(job_name)
                if job_description:
                    Job.setDescription(job_description)
                if project_name:
                    Job.setProjectName(project_name)
                if isinstance(workflow_variables, dict):
                    self.logger.debug('Adding variables')
                    job_variables = {}
                    for key, value in workflow_variables.items():
                        JobVariable = self.proactive_factory.create_job_variable()
                        JobVariable.setName(key)
                        JobVariable.setValue(value)
                        job_variables[key] = JobVariable
                    variables_java_map = MapConverter().convert(job_variables, self.runtime_gateway._gateway_client)
                    current_variables_java_map = Job.getVariables()
                    current_variables_python_dict = convert_java_map_to_python_dict(current_variables_java_map)
                    new_variables_python_dict = convert_java_map_to_python_dict(variables_java_map)
                    merged_variables_python_dict = {**current_variables_python_dict, **new_variables_python_dict}
                    merged_variables_java_map = MapConverter().convert(merged_variables_python_dict, self.runtime_gateway._gateway_client)
                    Job.setVariables(merged_variables_java_map)
                if isinstance(workflow_generic_info, dict):
                    self.logger.debug('Adding the generic information')
                    for key, value in workflow_generic_info.items():
                        Job.addGenericInformation(key, value)
                if isinstance(workflow_tags, list):
                    self.logger.debug('Adding tags')
                    workflow_tags_java_set = SetConverter().convert(workflow_tags, self.runtime_gateway._gateway_client)
                    Job.setWorkflowTags(workflow_tags_java_set)
                self.logger.info('Submitting the job ' + Job.getName())
                return self.proactive_scheduler_client.submit(Job).longValue()
        except Exception as e:
            self.logger.error("Error occurred while submitting the custom workflow from catalog", exc_info=True)
            return None

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

    def createTask(self, language=None, task_name=''):
        """
        Create a workflow task

        :param language: The script language
        :param task_name: The task name
        :return: A ProactiveTask object
        """
        self.logger.info('Creating a ' + str(language) + ' task')
        if language == self.proactive_script_language.python():
            return self.createPythonTask(task_name)
        else:
            return ProactiveTask(language, task_name) if self.proactive_script_language.is_language_supported(language) else None

    def createPythonTask(self, task_name='', default_python='python3'):
        """
        Creates a new task designed to execute Python scripts.

        :param task_name: The name of the task to be created.
        :param default_python: The default python to be used.
        :return: A ProactiveTask object set up for Python script execution.
        """
        self.logger.info('Creating a Python task')
        return ProactivePythonTask(task_name, default_python)

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

    def createJob(self, job_name=''):
        """
        Creates a new job with the specified name.

        :param job_name: The name of the job to be created.
        :return: A ProactiveJob object representing the newly created job.
        """
        self.logger.info('Creating a job')
        return ProactiveJob(job_name)

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
        Submits a job to the ProActive Scheduler.

        :param job_model: The job model to be submitted.
        :param debug: If True, prints the job configuration for debugging purposes.
        :return: The ID of the submitted job.
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

    def getTaskStatus(self, job_id, task_name):
        task_status = None
        job_state = self.getJobState(job_id)
        for task_state in job_state.getTasks():
            if task_state.getName() == task_name:
                task_status = str(task_state.getStatus().toString())
                break
        return task_status

    def getJobState(self, job_id):
        """
        Retrieves the current state of the specified job.

        :param job_id: The ID of the job.
        :return: The state of the job.
        """
        return self.proactive_scheduler_client.getJobState(str(job_id))

    def getJobStatus(self, job_id):
        """
        Retrieves the status of the specified job.

        :param job_id: The ID of the job to check.
        :return: The status of the job as a string.
        """
        return str(self.getJobState(str(job_id)).getJobInfo().getStatus().toString())

    def isJobFinished(self, job_id):
        """
        Checks if the specified job has finished execution.

        :param job_id: The ID of the job to check.
        :return: True if the job is finished, False otherwise.
        """
        return self.proactive_scheduler_client.isJobFinished(str(job_id))

    def isTaskFinished(self, job_id, task_name):
        """
        Checks if the specified task within a job has finished execution.

        :param job_id: The ID of the job containing the task.
        :param task_name: The name of the task to check.
        :return: True if the task is finished, False otherwise.
        """
        return self.proactive_scheduler_client.isTaskFinished(str(job_id), task_name)

    def getJobInfo(self, job_id):
        """
        Get the job info

        :param job_id: A valid job ID
        :return: The job info
        """
        return self.proactive_scheduler_client.getJobInfo(str(job_id))

    def waitForJob(self, job_id, timeout=60000):
        """
        Waits for a job to finish execution within the specified timeout.

        :param job_id: The ID of the job to wait for.
        :param timeout: The timeout in milliseconds. Default is 60000 milliseconds (1 minute).
        :return: The job info upon completion.
        """
        return self.proactive_scheduler_client.waitForJob(str(job_id), timeout)

    def waitJobIsFinished(self, job_id, time_to_check=.5):
        # Monitor job status
        is_finished = False
        while not is_finished:
            # Get the current state of the job
            job_status = self.getJobStatus(job_id)
            # Print the current job status
            self.logger.debug(f"Current job status: {job_status}")
            # Check if the job has finished
            if job_status.upper() in ["FINISHED", "CANCELED", "FAILED"]:
                is_finished = True
            else:
                # Wait before checking again
                time.sleep(time_to_check)

    def getAllJobs(self, max_number_of_jobs=1000, my_jobs_only=False, pending=False, running=True, finished=False,
                   withIssuesOnly=False, child_jobs=True, job_name=None, project_name=None, user_name=None, tenant=None, parent_id=None):
        """
        Retrieves a list of jobs from the ProActive scheduler based on the specified filters.

        :param max_number_of_jobs: The maximum number of jobs to retrieve.
        :param my_jobs_only: If True, only retrieves jobs submitted by the current user.
        :param pending: If True, includes jobs in PENDING state.
        :param running: If True, includes jobs in RUNNING state.
        :param finished: If True, includes jobs in FINISHED state.
        :param withIssuesOnly: If True, only includes jobs that have issues.
        :param child_jobs: If True, includes child jobs.
        :param job_name: Filters jobs by name.
        :param project_name: Filters jobs by project name.
        :param user_name: Filters jobs by the submitting user's name.
        :param tenant: Filters jobs by tenant.
        :param parent_id: Filters jobs by parent job ID.
        :return: A list of jobs matching the specified filters.
        """
        job_filter_criteria = self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.JobFilterCriteriaBuilder().myJobsOnly(my_jobs_only).pending(pending).running(running).finished(finished).withIssuesOnly(withIssuesOnly).childJobs(child_jobs).jobName(job_name).projectName(project_name).userName(user_name).tenant(tenant).parentId(parent_id).build()
        jobs_page = self.proactive_scheduler_client.getJobs(0, max_number_of_jobs, job_filter_criteria, None)
        return jobs_page.getList()

    @staticmethod
    def __decode__(value):
        return value.decode('ascii')

    def getJobOutput(self, job_id, timeout=-1):
        """
        Retrieves the output of the specified job. Can operate in blocking or non-blocking mode.

        :param job_id: The unique identifier of the job whose output is to be fetched.
        :param timeout: The maximum time in seconds to wait for job completion before fetching the output. 
                        A negative value indicates an indefinite wait (blocking mode).
        :return: The full log output of the job as a string.
        """
        if timeout < 0:
            self.logger.debug("Waiting job execution to be finished...")
            while not self.isJobFinished(str(job_id)):
                time.sleep(1)
            self.logger.debug("Getting job output...")
            job_output = self.getProactiveRestApi().get_job_log_full(job_id)
            return job_output
        else:
            return self.printJobOutput(job_id, timeout)

    def getJobResult(self, job_id, timeout=60000):
        """
        Retrieves the result of a completed job.

        :param job_id: The ID of the job to fetch the result for.
        :param timeout: The timeout in milliseconds for waiting for the job to finish.
        :return: The result of the job if available within the timeout period.
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

    def getJobResultMap(self, job_id, timeout=60000):
        """
        Retrieves the resultMap of a completed job.

        :param job_id: The ID of the job to fetch the result for.
        :param timeout: The timeout in milliseconds for waiting for the job to finish.
        :return: The result of the job if available within the timeout period.
        """
        return self.proactive_scheduler_client.waitForJob(str(job_id), timeout).getResultMap()

    def getJobPreciousResults(self, job_id, timeout=60000):
        """
        Retrieves the precious results of a completed job.

        :param job_id: The ID of the job to fetch the result for.
        :param timeout: The timeout in milliseconds for waiting for the job to finish.
        :return: The result of the job if available within the timeout period.
        """
        return self.proactive_scheduler_client.waitForJob(str(job_id), timeout).getPreciousResults()

    def getTaskResult(self, job_id, task_name, timeout=60000):
        """
        Retrieves the result of a specified task from a job.

        :param job_id: The ID of the job containing the task.
        :param task_name: The name of the task to fetch the result for.
        :param timeout: The timeout in milliseconds for waiting for the task to finish.
        :return: The result of the task if available within the timeout period.
        """
        self.logger.debug('Getting results of the task \'' + task_name + '\'')
        task_result = self.proactive_scheduler_client.waitForTask(str(job_id), task_name, timeout)
        self.logger.debug('Formatting results')
        if type(task_result.getValue()) is bytes:
            task_result = self.__decode__(task_result.getValue())
        return task_result.getValue()

    def getTaskPreciousResult(self, job_id, task_name, timeout=60000):
        """
        Retrieves the precious results of a specified task from a job.

        :param job_id: The ID of the job to fetch the result for.
        :param task_name: The name of the task to fetch the result for.
        :param timeout: The timeout in milliseconds for waiting for the job to finish.
        :return: The result of the job if available within the timeout period.
        """
        return self.proactive_scheduler_client.waitForJob(str(job_id), timeout).getPreciousResults().get(task_name).value()

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
        Exports the specified job to an XML representation.

        :param job_model: The job model to export.
        :param debug: If True, prints the job XML for debugging purposes.
        :return: The XML representation of the job.
        """
        proactive_job = self.buildJob(job_model, debug)
        self.logger.info('Transforming the job \'' + job_model.getJobName() + '\' to an XML string')
        Job2XMLTransformer = self.proactive_factory.create_job2xml_transformer()
        return Job2XMLTransformer.jobToxmlString(proactive_job)

    def saveJob2XML(self, job_model, xml_file_path, debug=False):
        """
        Saves the specified job model to an XML file.

        :param job_model: The job model to save.
        :param xml_file_path: The file path where the XML should be saved.
        :param debug: If True, prints the job XML to the console for debugging purposes.
        """
        self.logger.info('Saving the job \'' + job_model.getJobName() + '\' to the XML file \'' + xml_file_path + '\'')
        job_xml_data = self.exportJob2XML(job_model, debug)
        with open(xml_file_path, "w") as text_file:
            text_file.write("{0}".format(job_xml_data))

    def killJob(self, job_id):
        return self.proactive_scheduler_client.killJob(str(job_id))

    def killTask(self, job_id, task_name):
        return self.proactive_scheduler_client.killTask(str(job_id), task_name)

    def sendSignal(self, job_id, signal, variables):
        """
        Sends a signal to the specified job.

        :param job_id: The ID of the job to send the signal to.
        :param timeout: The name of the signal to be sent.
        :param variables: A dictionary containing variables names and values to be sent with the signal.
        :return: True if the signal is sent successfully, False otherwise.
        """
        sessionid = self.proactive_scheduler_client.getSession()
        url = '{}/rest/scheduler/job/{}/signals?signal={}'.format(self.base_url, job_id, signal)
        headers = {
            'sessionid': sessionid,
            'Content-Type': 'application/json'
        } 
        # Make the POST request
        response = requests.post(url, headers=headers, json=variables)
        # Check the response
        if response.status_code == 200:
            self.logger.info('Signal sent successfully.')
            return True
        else:
            self.logger.info('Failed to send signal. Status code: {}, Response: {}'.format(response.status_code, response.text))
            return False

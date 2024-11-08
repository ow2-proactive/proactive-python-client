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

from .monitoring.ProactiveNodeMBeanClient import ProactiveNodeMBeanClient

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
        Args:
            base_url (str): The base URL of the ProActive server
            debug (bool, optional): Enables debug mode for additional logging. Defaults to False
            javaopts (list, optional): Additional options for the Java virtual machine. Defaults to []
            log4j_props_file (str, optional): Path to the log4j properties file. Defaults to None
            log4py_props_file (str, optional): Path to the log4py properties file. Defaults to None
        Returns:
            None
        """
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.current_path = self.root_dir + "/java/lib/*"
        self.base_url = base_url
        self.gateway = JavaGateway()
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
        self.proactive_rest_api = ProactiveRestApi()
        self.proactive_monitoring_client = ProactiveNodeMBeanClient(self)

    def connect(self, username=None, password=None, credentials_path=None, insecure=True):
        """
        Connects to the ProActive server using provided credentials.
        Args:
            username (str, optional): Username for authentication. Defaults to None
            password (str, optional): Password for authentication. Defaults to None
            credentials_path (str, optional): Path to credentials file. Defaults to None
            insecure (bool, optional): If True, skips SSL certificate verification. Defaults to True
        Returns:
            None
        Raises:
            ConnectionError: If connection to the server fails
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
        try:
            self.proactive_scheduler_client.init(connection_info)
            self.proactive_rest_api.init(connection_info)
            self.logger.debug('Connected on ' + self.base_url)
        except Exception as e:
            self.logger.error('Failed to connect to ProActive server: {}'.format(str(e)))
            raise ConnectionError('Failed to connect to ProActive server: {}'.format(str(e)))

    def isConnected(self):
        """
        Checks if the gateway is currently connected to the ProActive server.
        Args:
            None
        Returns:
            bool: True if connected, False otherwise
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

    def getSession(self):
        """
        Get the current session ID for the ProActive client
        Args:
            None
        Returns:
            str: The current session ID
        """
        return self.proactive_scheduler_client.getSession()

    def getBaseURL(self):
        """
        Get the base URL of the ProActive server
        Args:
            None
        Returns:
            str: The base URL of the ProActive server
        """
        return self.base_url

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

    def getProactiveMonitoringClient(self):
        return self.proactive_monitoring_client

    def getRuntimeGateway(self):
        return self.runtime_gateway

    def getBucket(self, bucket_name):
        self.logger.debug('Returning the bucket: ' + bucket_name)
        return ProactiveBucketFactory().getBucket(self, bucket_name)

    def submitWorkflowFromCatalog(self, bucket_name, workflow_name, workflow_variables={}, workflow_generic_info={}):
        """
        Submits a workflow from the ProActive catalog to the scheduler.
        Args:
            bucket_name (str): Name of the bucket containing the workflow
            workflow_name (str): Name of the workflow to submit
            workflow_variables (dict, optional): Variables to pass to the workflow. Defaults to {}
            workflow_generic_info (dict, optional): Generic information for the workflow. Defaults to {}
        Returns:
            int: ID of the submitted job
        Raises:
            ValueError: If bucket or workflow name is invalid
            RuntimeError: If submission fails
        """
        workflow_variables_java_map = MapConverter().convert(workflow_variables, self.runtime_gateway._gateway_client)
        workflow_generic_info_java_map = MapConverter().convert(workflow_generic_info, self.runtime_gateway._gateway_client)
        self.logger.debug('Submitting from catalog the job \'' + bucket_name + '/' + workflow_name + '\'')
        return self.proactive_scheduler_client.submitFromCatalog(self.base_url + "/catalog", bucket_name, workflow_name, workflow_variables_java_map, workflow_generic_info_java_map).longValue()

    def submitWorkflowFromFile(self, workflow_xml_file_path, workflow_variables={}):
        """
        Submits a workflow from an XML file to the scheduler.
        The job will execute tasks as soon as resources are available.
        The job is considered finished once all tasks have completed (with either error or success).
        Args:
            workflow_xml_file_path (str): Path to the workflow XML file
            workflow_variables (dict, optional): Variables to pass to the workflow. Defaults to {}
        Returns:
            int: ID of the submitted job
        Raises:
            NotConnectedException: If the client is not connected to the scheduler
            PermissionException: If the user does not have permission to submit a job
            SubmissionClosedException: If job submission is not possible (e.g. scheduler is stopped)
            JobCreationException: If there was an error creating the job
        """
        workflow_variables_java_map = MapConverter().convert(workflow_variables, self.runtime_gateway._gateway_client)
        self.logger.debug('Submitting from file the job \'' + workflow_xml_file_path + '\'')
        return self.proactive_scheduler_client.submit(self.runtime_gateway.jvm.java.io.File(workflow_xml_file_path), workflow_variables_java_map).longValue()

    def submitCustomWorkflowFromFile(self, workflow_xml_file_path, workflow_variables=None, workflow_generic_info=None, job_name=None, job_description=None, project_name=None, bucket_name=None, label=None, workflow_tags=None):
        """
        Submits a customized workflow from an XML file to the scheduler with additional configuration options.
        Args:
            workflow_xml_file_path (str): Path to the workflow XML file
            workflow_variables (dict, optional): Variables to pass to the workflow. Defaults to None
            workflow_generic_info (dict, optional): Generic information for the workflow. Defaults to None
            job_name (str, optional): Custom name for the job. Defaults to None
            job_description (str, optional): Description of the job. Defaults to None
            project_name (str, optional): Name of the project the job belongs to. Defaults to None
            bucket_name (str, optional): Name of the bucket to associate with the job. Defaults to None
            label (str, optional): Label to assign to the job. Defaults to None
            workflow_tags (list, optional): List of tags to associate with the workflow. Defaults to None
        Returns:
            int: ID of the submitted job
        Raises:
            NotConnectedException: If the client is not connected to the scheduler
            PermissionException: If the user does not have permission to submit a job
            SubmissionClosedException: If job submission is not possible
            JobCreationException: If there was an error creating the job
        """
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
        """
        Submits a customized workflow from the ProActive catalog with additional configuration options.
        This method allows for more granular control over the workflow submission process by providing
        options to modify job properties, variables, and metadata before submission.
        Args:
            bucket_name (str): Name of the bucket containing the workflow to be submitted.
            workflow_name (str): Name of the workflow to submit from the catalog.
            workflow_variables (dict, optional): Dictionary of workflow variables where:
                - key (str): Variable name
                - value (str): Variable value
                Defaults to None.
            workflow_generic_info (dict, optional): Dictionary of generic information for the workflow where:
                - key (str): Information name
                - value (str): Information value 
                Defaults to None.
            job_name (str, optional): Custom name to assign to the job. If not provided,
                the original workflow name will be used. Defaults to None.
            job_description (str, optional): Description to assign to the job.
                Defaults to None.
            project_name (str, optional): Name of the project to associate with the job.
                Defaults to None.
            workflow_tags (list, optional): List of string tags to associate with the workflow.
                Defaults to None.
            local_file_path (str, optional): Path where a local copy of the workflow XML file
                should be saved. If provided, creates a copy of the workflow file at this location.
                Defaults to None.
        Returns:
            int: Job ID of the submitted workflow if successful, None if submission fails.
        Raises:
            Exception: If there is an error during workflow retrieval or submission.
                Common causes include:
                - Invalid bucket name or workflow name
                - Network connectivity issues
                - Permission issues
                - Invalid workflow variables or generic info format
        Note:
            - The method first retrieves the workflow from the catalog, then applies any
            custom configurations before submission.
            - If local_file_path is provided, a copy of the workflow XML will be saved
            before submission, which can be useful for debugging or version control.
            - All variables and generic info values must be strings or be convertible to strings.
        """
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
        Submits a workflow to the ProActive scheduler from a URL location.
        This method downloads and submits a workflow definition from a specified URL,
        allowing for remote workflow deployment.
        Args:
            workflow_url_spec (str): The complete URL to the workflow definition file.
                The URL must be accessible from the ProActive server and point to a valid
                workflow XML file.
            workflow_variables (dict, optional): Dictionary of variables to pass to the workflow where:
                - key (str): Variable name
                - value (str): Variable value
                Defaults to an empty dictionary.
        Returns:
            int: The job ID of the submitted workflow as a long integer value.
                This ID can be used to monitor and manage the job after submission.
        Raises:
            NotConnectedException: If not connected to the ProActive scheduler
            PermissionException: If user lacks permissions to submit jobs
            SubmissionClosedException: If the scheduler is not accepting job submissions
            JobCreationException: If the workflow XML is invalid or cannot be processed
            MalformedURLException: If the provided URL is invalid or malformed
            IOException: If there are network issues accessing the URL
        Note:
            - The workflow file at the specified URL must be in valid ProActive XML format
            - The URL must be accessible from the ProActive server, not just the client
            - All workflow variables must be strings or be convertible to strings
            - The method converts the workflow variables to a Java map internally
            - The returned job ID can be used with other methods like getJobStatus() or waitForJob()
        """
        workflow_variables_java_map = MapConverter().convert(workflow_variables, self.runtime_gateway._gateway_client)
        self.logger.debug('Submitting from URL the job \'' + workflow_url_spec + '\'')
        return self.proactive_scheduler_client.submit(self.runtime_gateway.jvm.java.net.URL(workflow_url_spec), workflow_variables_java_map).longValue()

    def createTask(self, language=None, task_name=''):
        """
        Creates a new task for executing scripts in a specified programming language.
        For Python tasks, it creates a specialized Python task object. For other
        supported languages, it creates a standard ProactiveTask object.
        Args:
            language (str, optional): The programming language for the task's script.
                Must be one of the languages supported by the ProActive scheduler.
                For Python tasks, use the value returned by proactive_script_language.python().
                Defaults to None.
            task_name (str, optional): Name to assign to the task. If not provided,
                an empty string will be used. Defaults to ''.
        Returns:
            Union[ProactiveTask, ProactivePythonTask, None]: 
                - A ProactivePythonTask object if language is Python
                - A ProactiveTask object if language is supported but not Python
                - None if the specified language is not supported
        Note:
            - Python tasks are handled specially through the createPythonTask() method
            which provides additional Python-specific configurations
            - The language must be one of the supported script languages in the
            ProActive environment, which can be checked using
            proactive_script_language.is_language_supported()
            - You can get the list of supported languages through the
            getProactiveScriptLanguage() method
        """
        self.logger.info('Creating a ' + str(language) + ' task')
        if language == self.proactive_script_language.python():
            return self.createPythonTask(task_name)
        else:
            return ProactiveTask(language, task_name) if self.proactive_script_language.is_language_supported(language) else None

    def createPythonTask(self, task_name='', default_python='python3'):
        """
        Creates a specialized ProActiveTask object configured specifically for Python script execution.
        This method provides a convenient way to create tasks that will run Python code in the
        ProActive environment.
        Args:
            task_name (str, optional): Name to assign to the task. This name will be used to 
                identify the task in the workflow and in monitoring tools. If not provided,
                defaults to an empty string and a system-generated name will be used.
            default_python (str, optional): The Python command or executable path to use for task
                execution. Specifies which Python interpreter should be used to run the task.
                Defaults to 'python3'. Common values include:
                - 'python3': Use Python 3.x
                - 'python': Use system default Python
                - '/usr/bin/python3.8': Use specific Python version/path
        Returns:
            ProactivePythonTask: A task object specifically configured for Python execution.
        Note:
            - The Python environment used must have all required dependencies installed
            - The selected Python version must be available on the execution nodes
            - Task names should be unique within a workflow
            - The task is not executed until it is added to a job and the job is submitted
            - Python tasks automatically handle proper script formatting and environment setup
            - You can access task results and output after execution using task_id
        """
        self.logger.info('Creating a Python task ' + task_name)
        return ProactivePythonTask(task_name, default_python)

    def createFlowScript(self, script_language=None):
        """
        Creates a flow script for controlling workflow execution.
        Args:
            script_language (str, optional): Language to use for the flow script. If not provided,
                defaults to JavaScript.
        Returns:
            ProactiveFlowScript: A flow script object that can be used to control workflow execution
        """
        if script_language is None:
            script_language = self.proactive_script_language.javascript()
        self.logger.info('Creating a flow script')
        return ProactiveFlowScript(script_language)

    def createReplicateFlowScript(self, script_implementation, script_language="javascript"):
        """
        Creates a flow script that replicates tasks in the workflow.
        Args:
            script_implementation (str): The script code to be executed for replication
            script_language (str, optional): Language to use for the flow script. Defaults to "javascript"
        Returns:
            ProactiveFlowScript: A flow script object configured for task replication
        """
        self.logger.info('Creating a Replicate flow script')
        flow_script = ProactiveFlowScript(script_language)
        flow_script.setActionType(self.proactive_flow_action_type.replicate())
        flow_script.setImplementation(script_implementation)
        return flow_script

    def createLoopFlowScript(self, script_implementation, target, script_language="javascript"):
        """
        Creates a flow script that implements a loop in the workflow.
        Args:
            script_implementation (str): The script code to be executed for the loop
            target (str): The target task name that the loop should jump back to
            script_language (str, optional): Language to use for the flow script. Defaults to "javascript"
        Returns:
            ProactiveFlowScript: A flow script object configured for loop control
        """
        self.logger.info('Creating a Loop flow script')
        flow_script = ProactiveFlowScript(script_language)
        flow_script.setActionType(self.proactive_flow_action_type.loop())
        flow_script.setImplementation(script_implementation)
        flow_script.setActionTarget(target)
        return flow_script

    def createBranchFlowScript(self, script_implementation, target_if, target_else, target_continuation, script_language="javascript"):
        """
        Creates a flow script that implements branching logic in the workflow.
        Args:
            script_implementation (str): The script code to be executed for the branch condition
            target_if (str): Name of the task to execute if condition is true
            target_else (str): Name of the task to execute if condition is false 
            target_continuation (str): Name of the task to execute after the branch completes
            script_language (str, optional): Language to use for the flow script. Defaults to "javascript"
        Returns:
            ProactiveFlowScript: A flow script object configured for branch control
        Raises:
            ValueError: If any of the target task names are invalid
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
        Gets the ProActive flow block type.
        Args:
            None
        Returns:
            ProactiveFlowBlock: The ProactiveFlowBlock object
        """
        return self.proactive_flow_block

    def createPreScript(self, language=None):
        """
        Creates a pre-script for a ProActive task.
        Args:
            language (str, optional): Language to use for the pre-script. Defaults to None
        Returns:
            ProactivePreScript: A pre-script object if language is supported, None otherwise
        """
        self.logger.info('Creating a pre script')
        return ProactivePreScript(language) if self.proactive_script_language.is_language_supported(language) else None

    def createPostScript(self, language=None):
        """
        Creates a post-script for a ProActive task.
        Args:
            language (str, optional): Language to use for the post-script. Defaults to None
        Returns:
            ProactivePostScript: A post-script object if language is supported, None otherwise
        """
        self.logger.info('Creating a post script')
        return ProactivePostScript(language) if self.proactive_script_language.is_language_supported(language) else None

    def createJob(self, job_name=''):
        """
        Creates a new job with the specified name.
        Args:
            job_name (str, optional): Name for the job. Defaults to ''
        Returns:
            ProactiveJob: A ProactiveJob object representing the newly created job
        """
        self.logger.info('Creating a job')
        return ProactiveJob(job_name)

    def buildJob(self, job_model, debug=False):
        """
        Builds a ProActive job to be submitted to the scheduler.
        Args:
            job_model: A valid job model
            debug (bool, optional): If True, prints the job configuration for debugging. Defaults to False
        Returns:
            ProactiveJob: A ProActive job ready to be submitted
        """
        self.logger.info('Building the job ' + job_model.getJobName())
        return ProactiveJobBuilder(self.proactive_factory, job_model, self.debug, self.log4py_props_file).create().display(debug).getProactiveJob()

    def submitJob(self, job_model, debug=False):
        """
        Submits a job to the ProActive Scheduler.
        Args:
            job_model: The job model to be submitted
            debug (bool, optional): If True, prints the job configuration for debugging. Defaults to False
        Returns:
            int: ID of the submitted job
        Raises:
            NotConnectedException: If the client is not connected to the scheduler
            PermissionException: If the user does not have permission to submit a job
            SubmissionClosedException: If job submission is not possible (e.g. scheduler is stopped)
            JobCreationException: If there was an error creating the job
        """
        proactive_job = self.buildJob(job_model, debug)
        self.logger.info('Submitting the job ' + job_model.getJobName())
        return self.proactive_scheduler_client.submit(proactive_job).longValue()

    def submitJobWithInputsAndOutputsPaths(self, job_model, input_folder_path='.', output_folder_path='.', debug=False):
        """
        Submits a job to the ProActive Scheduler with specified input and output paths.
        Args:
            job_model: A valid job model
            input_folder_path (str, optional): Path to the directory containing input files. Defaults to '.'
            output_folder_path (str, optional): Path to the local directory which will contain output files. Defaults to '.'
            debug (bool, optional): If True, prints the job configuration for debugging. Defaults to False
        Returns:
            int: ID of the submitted job
        Raises:
            NotConnectedException: If the client is not connected to the scheduler
            PermissionException: If the user does not have permission to submit a job
            SubmissionClosedException: If job submission is not possible (e.g. scheduler is stopped)
            JobCreationException: If there was an error creating the job
        """
        proactive_job = self.buildJob(job_model, debug)
        self.logger.info('Submitting the job ' + job_model.getJobName())
        return self.proactive_scheduler_client.submit(
            proactive_job,
            input_folder_path,
            output_folder_path,
            False,
            True
        ).longValue()

    def createForkEnvironment(self, language=None):
        """
        Creates a ProActive fork environment.
        Args:
            language (str, optional): The script language to use. Defaults to None
        Returns:
            ProactiveForkEnv: A ProActive fork environment object
        """
        self.logger.info('Creating a fork environment')
        return ProactiveForkEnv(language) if self.proactive_script_language.is_language_supported(language) else None

    def createDefaultForkEnvironment(self):
        """
        Creates a default fork environment.
        Args:
            None
        Returns:
            ProactiveForkEnv: A default ProActive fork environment object
        """
        self.logger.info('Creating a default fork environment')
        return ProactiveForkEnv(self.proactive_script_language.jython())

    def createPythonForkEnvironment(self):
        """
        Creates a Python fork environment.
        Args:
            None
        Returns:
            ProactiveForkEnv: A Python ProActive fork environment object
        """
        self.logger.info('Creating a Python fork environment')
        return ProactiveForkEnv(self.proactive_script_language.python())

    def createSelectionScript(self, language=None):
        """
        Creates a ProActive selection script.
        Args:
            language (str, optional): The script language to use. Defaults to None
        Returns:
            ProactiveSelectionScript: A ProActive selection script object
        """
        self.logger.info('Creating a selection script')
        return ProactiveSelectionScript(language) if self.proactive_script_language.is_language_supported(language) else None

    def createDefaultSelectionScript(self):
        """
        Creates a default selection script.
        Args:
            None
        Returns:
            ProactiveSelectionScript: A default ProActive selection script object
        """
        self.logger.info('Creating a default selection script')
        return ProactiveSelectionScript(self.proactive_script_language.jython())

    def createPythonSelectionScript(self):
        """
        Creates a Python selection script.
        Args:
            None
        Returns:
            ProactiveSelectionScript: A Python ProActive selection script object
        """
        self.logger.info('Creating a Python selection script')
        return ProactiveSelectionScript(self.proactive_script_language.python())

    def getProactiveClient(self):
        """
        Gets the ProActive scheduler client.
        Args:
            None
        Returns:
            SmartProxyClient: The ProActive scheduler client object
        """
        return self.proactive_scheduler_client

    def getProactiveScriptLanguage(self):
        """
        Gets the ProActive script language object.
        Args:
            None
        Returns:
            ProactiveScriptLanguage: The ProActive script language object
        """
        return self.proactive_script_language

    def getTaskStatus(self, job_id, task_name):
        """
        Retrieves the status of a specific task within a job.
        Args:
            job_id (str): ID of the job containing the task
            task_name (str): Name of the task to check
        Returns:
            str: Status of the task, or None if task not found
        Raises:
            ValueError: If job_id or task_name is invalid
            RuntimeError: If status cannot be retrieved
        """
        task_status = None
        job_state = self.getJobState(job_id)
        for task_state in job_state.getTasks():
            if task_state.getName() == task_name:
                task_status = str(task_state.getStatus().toString())
                break
        return task_status

    def getJobState(self, job_id):
        """
        Retrieves the current state of a job.
        Args:
            job_id (str): ID of the job to check
        Returns:
            JobState: Current state of the job
        Raises:
            ValueError: If job_id is invalid
            RuntimeError: If state cannot be retrieved
        """
        return self.proactive_scheduler_client.getJobState(str(job_id))

    def getJobStatus(self, job_id):
        """
        Retrieves the status of the specified job.
        Args:
            job_id (str): The ID of the job to check
        Returns:
            str: The status of the job
        Raises:
            ValueError: If job_id is invalid
            RuntimeError: If status cannot be retrieved
        """
        return str(self.getJobState(str(job_id)).getJobInfo().getStatus().toString())

    def isJobFinished(self, job_id):
        """
        Checks if the specified job has finished execution.
        Args:
            job_id (str): ID of the job to check
        Returns:
            bool: True if the job is finished, False otherwise
        Raises:
            ValueError: If job_id is invalid
            RuntimeError: If status cannot be retrieved
        """
        return self.proactive_scheduler_client.isJobFinished(str(job_id))

    def isTaskFinished(self, job_id, task_name):
        """
        Checks if the specified task within a job has finished execution.
        Args:
            job_id (str): The ID of the job containing the task
            task_name (str): The name of the task to check
        Returns:
            bool: True if the task is finished, False otherwise
        Raises:
            ValueError: If job_id or task_name is invalid
            RuntimeError: If status cannot be retrieved
        """
        return self.proactive_scheduler_client.isTaskFinished(str(job_id), task_name)

    def getJobInfo(self, job_id):
        """
        Retrieves information about a specific job.
        Args:
            job_id (str): ID of the job to get information for
        Returns:
            JobInfo: Information about the specified job
        Raises:
            ValueError: If job_id is invalid
            RuntimeError: If job info cannot be retrieved
        """
        return self.proactive_scheduler_client.getJobInfo(str(job_id))

    def waitForJob(self, job_id, timeout=60000):
        """
        Waits for a job to finish execution within the specified timeout.
        Args:
            job_id (str): The ID of the job to wait for
            timeout (int, optional): The timeout in milliseconds. Defaults to 60000 milliseconds (1 minute)
        Returns:
            JobInfo: Information about the completed job
        Raises:
            TimeoutException: If the timeout is reached before job completion
            RuntimeError: If waiting for the job fails
        """
        return self.proactive_scheduler_client.waitForJob(str(job_id), timeout)

    def waitJobIsFinished(self, job_id, time_to_check=0.5):
        """
        Waits for a job to finish execution by polling its status.
        Args:
            job_id (str): The ID of the job to wait for
            time_to_check (float, optional): Time in seconds to wait between status checks. Defaults to 0.5
        Returns:
            None
        Raises:
            ValueError: If job_id is invalid
            RuntimeError: If job status cannot be retrieved
        """
        # Monitor job status
        is_finished = False
        while not is_finished:
            # Get the current state of the job
            job_status = self.getJobStatus(job_id)
            # Print the current job status
            self.logger.debug("Current job status: {0}".format(job_status))
            # Check if the job has finished
            if job_status.upper() in ["FINISHED", "CANCELED", "FAILED"]:
                is_finished = True
            else:
                # Wait before checking again
                time.sleep(time_to_check)

    def getAllJobs(self, max_number_of_jobs=1000, my_jobs_only=False, pending=False, running=True, finished=False, withIssuesOnly=False, child_jobs=True, job_name=None, project_name=None, user_name=None, tenant=None, parent_id=None):
        """
        Retrieves a list of jobs from the ProActive scheduler based on the specified filters.
        Args:
            max_number_of_jobs (int, optional): The maximum number of jobs to retrieve. Defaults to 1000
            my_jobs_only (bool, optional): If True, only retrieves jobs submitted by the current user. Defaults to False
            pending (bool, optional): If True, includes jobs in PENDING state. Defaults to False
            running (bool, optional): If True, includes jobs in RUNNING state. Defaults to True
            finished (bool, optional): If True, includes jobs in FINISHED state. Defaults to False
            withIssuesOnly (bool, optional): If True, only includes jobs that have issues. Defaults to False
            child_jobs (bool, optional): If True, includes child jobs. Defaults to True
            job_name (str, optional): Filters jobs by name. Defaults to None
            project_name (str, optional): Filters jobs by project name. Defaults to None
            user_name (str, optional): Filters jobs by the submitting user's name. Defaults to None
            tenant (str, optional): Filters jobs by tenant. Defaults to None
            parent_id (str, optional): Filters jobs by parent job ID. Defaults to None
        Returns:
            list: A list of jobs matching the specified filters
        Raises:
            RuntimeError: If retrieving jobs fails
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
        Args:
            job_id (int): The unique identifier of the job whose output is to be fetched
            timeout (int, optional): The maximum time in seconds to wait for job completion before fetching the output.
                A negative value indicates an indefinite wait (blocking mode). Defaults to -1
        Returns:
            str: The full log output of the job
        Raises:
            ValueError: If job_id is invalid
            RuntimeError: If job output cannot be retrieved
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
        Args:
            job_id (int): The ID of the job to fetch the result for
            timeout (int, optional): The timeout in milliseconds for waiting for the job to finish. Defaults to 60000
        Returns:
            str: The combined results of all tasks in the job as a string
        Raises:
            RuntimeError: If job results cannot be retrieved
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
        Args:
            job_id (int): The ID of the job to fetch the result for
            timeout (int, optional): The timeout in milliseconds for waiting for the job to finish. Defaults to 60000
        Returns:
            dict: The result map containing task results from the completed job
        Raises:
            RuntimeError: If job results cannot be retrieved
        """
        return self.proactive_scheduler_client.waitForJob(str(job_id), timeout).getResultMap()

    def getJobPreciousResults(self, job_id, timeout=60000):
        """
        Retrieves the precious results of a completed job.
        Args:
            job_id (int): The ID of the job to fetch the result for
            timeout (int, optional): The timeout in milliseconds for waiting for the job to finish. Defaults to 60000
        Returns:
            dict: The precious results from the completed job
        Raises:
            RuntimeError: If job results cannot be retrieved
        """
        return self.proactive_scheduler_client.waitForJob(str(job_id), timeout).getPreciousResults()

    def getTaskResult(self, job_id, task_name, timeout=60000):
        """
        Retrieves the result of a specified task from a job.
        Args:
            job_id (int): The ID of the job containing the task
            task_name (str): The name of the task to fetch the result for
            timeout (int, optional): The timeout in milliseconds for waiting for the task to finish. Defaults to 60000
        Returns:
            Any: The result of the task if available within the timeout period
        Raises:
            RuntimeError: If task result cannot be retrieved
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
        Args:
            job_id (int): The ID of the job to fetch the result for
            task_name (str): The name of the task to fetch the result for
            timeout (int, optional): The timeout in milliseconds for waiting for the job to finish. Defaults to 60000
        Returns:
            Any: The precious result of the task if available within the timeout period
        Raises:
            RuntimeError: If task result cannot be retrieved
        """
        return self.proactive_scheduler_client.waitForJob(str(job_id), timeout).getPreciousResults().get(task_name).value()

    def printJobOutput(self, job_id, timeout=60000):
        """
        Retrieves and formats the output logs from all tasks in a job.
        Args:
            job_id (int): The ID of the job to fetch outputs for
            timeout (int, optional): The timeout in milliseconds for waiting for the job to finish. Defaults to 60000
        Returns:
            str: The concatenated stdout logs from all tasks in the job, with each task's output separated by newlines
        Raises:
            RuntimeError: If job outputs cannot be retrieved
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
        Retrieves the output logs from a specific task in a job.
        Args:
            job_id (int): The ID of the job containing the task
            task_name (str): The name of the task to fetch outputs for
            timeout (int, optional): The timeout in milliseconds for waiting for the task to finish. Defaults to 60000
        Returns:
            str: The stdout logs from the specified task, with whitespace trimmed
        Raises:
            RuntimeError: If task outputs cannot be retrieved
        """
        self.logger.debug('Getting the task \'' + task_name + '\'\'s outputs')
        task_output = self.proactive_scheduler_client.waitForTask(str(job_id), task_name, timeout).getOutput()
        return task_output.getStdoutLogs().strip(' \n')

    def exportJob2XML(self, job_model, debug=False):
        """
        Exports the specified job to an XML representation.
        Args:
            job_model: The job model to export
            debug (bool, optional): If True, prints the job XML for debugging purposes. Defaults to False
        Returns:
            str: The XML representation of the job
        """
        proactive_job = self.buildJob(job_model, debug)
        self.logger.info('Transforming the job \'' + job_model.getJobName() + '\' to an XML string')
        Job2XMLTransformer = self.proactive_factory.create_job2xml_transformer()
        return Job2XMLTransformer.jobToxmlString(proactive_job)

    def saveJob2XML(self, job_model, xml_file_path, debug=False):
        """
        Saves the specified job model to an XML file.
        Args:
            job_model: The job model to save
            xml_file_path (str): The file path where the XML should be saved
            debug (bool, optional): If True, prints the job XML to the console for debugging purposes. Defaults to False
        Returns:
            None
        Raises:
            IOError: If the XML file cannot be written
        """
        self.logger.info('Saving the job \'' + job_model.getJobName() + '\' to the XML file \'' + xml_file_path + '\'')
        job_xml_data = self.exportJob2XML(job_model, debug)
        with open(xml_file_path, "w") as text_file:
            text_file.write("{0}".format(job_xml_data))

    def killJob(self, job_id):
        """Kills a job and all its running tasks.
        This method will kill all running tasks of the job and remove it from the scheduler.
        The job will not be terminated normally and will not produce results.
        Only the job owner can kill their jobs.
        Args:
            job_id (str): The ID of the job to kill.
        Returns:
            bool: True if the job was successfully killed, False otherwise
        Raises:
            NotConnectedException: If not authenticated
            UnknownJobException: If the specified job does not exist
            PermissionException: If user lacks permissions to kill this job
        """
        return self.proactive_scheduler_client.killJob(str(job_id))

    def pauseJob(self, job_id):
        """Pauses the execution of a job.
        This method will complete all currently running tasks of the job before pausing it.
        The job must be resumed explicitly to continue execution.
        Args:
            job_id (str): The ID of the job to pause.
        Returns:
            bool: True if the job was successfully paused, False otherwise
        Raises:
            NotConnectedException: If not authenticated
            UnknownJobException: If the specified job does not exist
            PermissionException: If user lacks permissions to pause this job
        Note:
            Users can only pause their own jobs.
        """
        return self.proactive_scheduler_client.pauseJob(str(job_id))

    def resumeJob(self, job_id):
        """Resumes the execution of a paused job.
        This method will restart all non-finished tasks of the job.
        Args:
            job_id (str): The ID of the job to resume.
        Returns:
            bool: True if the job was successfully resumed, False otherwise
        Raises:
            NotConnectedException: If not authenticated
            UnknownJobException: If the specified job does not exist
            PermissionException: If user lacks permissions to resume this job
        Note:
            Users can only resume their own jobs.
        """
        return self.proactive_scheduler_client.resumeJob(str(job_id))

    def killTask(self, job_id, task_name):
        """Attempts to kill a specific task within a job.
        Tries to kill the specified task if it exists and is running.
        Only the task owner can kill their tasks.
        Args:
            job_id (str): ID of the job containing the task to kill
            task_name (str): Name of the task to kill
        Returns:
            bool: True if task was successfully killed, False if task couldn't be killed (not running)
        Raises:
            NotConnectedException: If not authenticated
            UnknownJobException: If job does not exist
            UnknownTaskException: If task does not exist in job
            PermissionException: If lacking permissions to access job/task
        """
        return self.proactive_scheduler_client.killTask(str(job_id), task_name)

    def restartTask(self, job_id, task_name, delay_in_seconds=0):
        """Attempts to restart a task within a job.
        Restarts the specified task if it exists and is running. Only the task owner 
        can restart their tasks. The task will be terminated and rescheduled after 
        the specified delay.
        Possible outcomes after restart:
        - If task hasn't reached max executions: Rescheduled after delay
        - If task has reached max executions: Marked as faulty
        - If task has reached max executions with cancelJobOnError: Marked faulty and job terminates
        Args:
            job_id (str): ID of the job containing the task to restart.
            task_name (str): Name of the task to restart.
            delay_in_seconds (int, optional): Delay in seconds before task is eligible for rescheduling. Defaults to 0.
        Returns:
            bool: True if task was successfully restarted, False if task couldn't be restarted (not running)
        Raises:
            NotConnectedException: If not authenticated
            UnknownJobException: If job does not exist
            UnknownTaskException: If task does not exist in job
            PermissionException: If lacking permissions to access job/task
        """
        return self.proactive_scheduler_client.restartTask(str(job_id), task_name, delay_in_seconds)

    def preemptTask(self, job_id, task_name, delay_in_seconds=0):
        """Attempts to stop and restart a task execution within a job.
        Args:
            job_id (str): ID of the job containing the task to be stopped
            task_name (str): Name of the task to stop
            delay_in_seconds (int, optional): Delay between task termination and re-scheduling eligibility. Defaults to 0.
        Returns:
            bool: True if task was successfully stopped, False if task couldn't be stopped (not running)
        Raises:
            NotConnectedException: If not authenticated
            UnknownJobException: If job does not exist
            UnknownTaskException: If task does not exist in job
            PermissionException: If lacking permissions to access job/task
        """
        return self.proactive_scheduler_client.preemptTask(str(job_id), task_name, delay_in_seconds)

    def sendSignal(self, job_id, signal, variables):
        """
        Sends a signal to the specified job.
        Args:
            job_id (str): ID of the job to send the signal to
            signal (str): Name of the signal to be sent
            variables (dict): Dictionary containing variable names and values to be sent with the signal
        Returns:
            bool: True if signal was sent successfully, False otherwise
        Raises:
            ConnectionError: If connection to the server fails
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

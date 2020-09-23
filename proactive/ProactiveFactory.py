

class ProactiveFactory:
    """
    https://www.activeeon.com/public_content/documentation/javadoc/latest/index.html
    """

    def __init__(self, runtime_gateway=None):
        """
        Create a Proactive factory

        :param runtime_gateway: A valid java runtime gateway
        """
        self.setRuntimeGateway(runtime_gateway)

    def setRuntimeGateway(self, runtime_gateway=None):
        """
        Set the Proactive java runtime gateway

        :param runtime_gateway: A valid java runtime gateway
        """
        self.runtime_gateway = runtime_gateway

    def getRuntimeGateway(self):
        """
        Get the java runtime gateway

        :return: The java runtime gateway
        """
        return self.runtime_gateway

    def create_smart_proxy(self):
        """
        Create a ProActive smart proxy
        https://doc.activeeon.com/javadoc/latest/org/ow2/proactive_grid_cloud_portal/smartproxy/RestSmartProxyImpl.html

        :return: A RestSmartProxyImpl object
        """
        return self.runtime_gateway.jvm.org.ow2.proactive_grid_cloud_portal.smartproxy.RestSmartProxyImpl()

    def create_connection_info(self, url, username, password, credentials_file, insecure):
        """
        Create a ProActive connection info
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/authentication/ConnectionInfo.html

        :param url: The ProActive server URL
        :param username: A valid username
        :param password: A valid password
        :param credentials_file: A credentials file path
        :param insecure: If set True, the connection is set to the insecure mode
        :return: A ConnectionInfo object
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.authentication.ConnectionInfo(
            url, username, password, credentials_file, insecure
        )

    def create_simple_script(self, script_code, script_language):
        """
        Create a ProActive simple script
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scripting/SimpleScript.html

        :param script_code: The script implementation
        :param script_language: The script language
        :return: A SimpleScript object
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scripting.SimpleScript(script_code, script_language)

    def create_flow_script(self, script):
        """
        Create a ProActive flow script
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/flow/FlowScript.html

        :param script: A valid flow action
        :return: A FlowScript object
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.flow.FlowScript(script)

    def get_flow_script(self):
        """
        Get the ProActive flow script Class
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/flow/FlowScript.html

        :return: The FlowScript Class
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.flow.FlowScript

    def get_flow_block(self):
        """
        Get the ProActive flow block Class
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/flow/FlowBlock.html

        :return: The FlowBlock Class
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.flow.FlowBlock

    def create_task_script(self, simple_script):
        """
        Create a ProActive task script
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scripting/TaskScript.html

        :param simple_script: A valid simple script
        :return: A TaskScript object
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scripting.TaskScript(simple_script)

    def create_script_task(self):
        """
        Create a ProActive script task
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/ScriptTask.html

        :return: A ScriptTask object
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.ScriptTask()

    def create_job(self):
        """
        Create a ProActive job
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/job/TaskFlowJob.html

        :return: A TaskFlowJob object
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.job.TaskFlowJob()

    def create_fork_environment(self):
        """
        Create a ProActive fork environment
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/ForkEnvironment.html

        :return: A ForkEnvironment object
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.ForkEnvironment()

    def create_selection_script(self, script_code, script_language, is_dynamic):
        """
        Create a ProActive selection script
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scripting/SelectionScript.html

        :param script_code: The selection script implementation
        :param script_language: The selection script language
        :param is_dynamic: If set True, the selection script will be set as dynamic
        :return: A SelectionScript object
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scripting.SelectionScript(script_code, script_language, is_dynamic)

    def create_job_variable(self):
        """
        Create a ProActive job variable
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/job/JobVariable.html

        :return: A JobVariable object
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.job.JobVariable()

    def create_task_variable(self):
        """
        Create a task variable
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/TaskVariable.html

        :return: A TaskVariable object
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.TaskVariable()

    def get_input_access_mode(self):
        """
        Get the ProActive input access mode Class
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/dataspaces/InputAccessMode.html

        :return: The InputAccessMode Class
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.dataspaces.InputAccessMode

    def get_output_access_mode(self):
        """
        Get the ProActive output access mode Class
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/dataspaces/OutputAccessMode.html

        :return: The OutputAccessMode Class
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.dataspaces.OutputAccessMode

    def create_job2xml_transformer(self):
        """
        Create a ProActive job to XML transformer
        https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/job/factories/Job2XMLTransformer.html

        :return: A Job2XMLTransformer object
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.job.factories.Job2XMLTransformer()


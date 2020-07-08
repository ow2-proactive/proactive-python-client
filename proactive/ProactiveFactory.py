

"""
https://www.activeeon.com/public_content/documentation/javadoc/latest/index.html
"""
class ProactiveFactory:

    def __init__(self, runtime_gateway=None):
        self.setRuntimeGateway(runtime_gateway)

    def setRuntimeGateway(self, runtime_gateway=None):
        self.runtime_gateway = runtime_gateway

    def getRuntimeGateway(self):
        return self.runtime_gateway

    def create_smart_proxy(self):
        """
          https://doc.activeeon.com/javadoc/latest/org/ow2/proactive_grid_cloud_portal/smartproxy/RestSmartProxyImpl.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive_grid_cloud_portal.smartproxy.RestSmartProxyImpl()

    def create_connection_info(self, url, username, password, credentials_file, insecure):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/authentication/ConnectionInfo.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.authentication.ConnectionInfo(
            url, username, password, credentials_file, insecure
        )

    def create_simple_script(self, script_code, script_language):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scripting/SimpleScript.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scripting.SimpleScript(script_code, script_language)

    def create_flow_script(self, script):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/flow/FlowScript.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.flow.FlowScript(script)

    def get_flow_script(self):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/flow/FlowScript.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.flow.FlowScript

    def get_flow_block(self):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/flow/FlowBlock.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.flow.FlowBlock

    def create_task_script(self, simple_script):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scripting/TaskScript.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scripting.TaskScript(simple_script)

    def create_script_task(self):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/ScriptTask.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.ScriptTask()

    def create_job(self):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/job/TaskFlowJob.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.job.TaskFlowJob()

    def create_fork_environment(self):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/ForkEnvironment.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.ForkEnvironment()

    def create_selection_script(self, script_code, script_language, is_dynamic):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scripting/SelectionScript.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scripting.SelectionScript(script_code, script_language, is_dynamic)

    def create_job_variable(self):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/job/JobVariable.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.job.JobVariable()

    def create_task_variable(self):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/TaskVariable.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.TaskVariable()

    def get_input_access_mode(self):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/dataspaces/InputAccessMode.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.dataspaces.InputAccessMode

    def get_output_access_mode(self):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/task/dataspaces/OutputAccessMode.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.dataspaces.OutputAccessMode

    def create_job2xml_transformer(self):
        """
          https://www.activeeon.com/public_content/documentation/javadoc/latest/org/ow2/proactive/scheduler/common/job/factories/Job2XMLTransformer.html
        """
        return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.job.factories.Job2XMLTransformer()


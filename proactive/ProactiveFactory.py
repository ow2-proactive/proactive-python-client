

class ProactiveFactory:
  runtime_gateway = None

  def __init__(self, runtime_gateway):
    self.runtime_gateway = runtime_gateway

  def create_simple_script(self, script_code, script_language):
    return self.runtime_gateway.jvm.org.ow2.proactive.scripting.SimpleScript(script_code, script_language)

  def create_task_script(self, simple_script):
    return self.runtime_gateway.jvm.org.ow2.proactive.scripting.TaskScript(simple_script)

  def create_script_task(self):
    return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.ScriptTask()

  def create_job(self):
    return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.job.TaskFlowJob()

  def create_fork_environment(self):
    return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.ForkEnvironment()

  def create_selection_script(self, script_code, script_language, is_dynamic):
    return self.runtime_gateway.jvm.org.ow2.proactive.scripting.SelectionScript(script_code, script_language, is_dynamic)


import cloudpickle
import codecs


class SerialisationHelper:
  runtime_gateway = None
  """
  Simple client for the ProActive scheduler REST API
  See also https://try.activeeon.com/rest/doc/jaxrsdocs/overview-summary.html
  """

  def __init__(self, runtime_gateway):
    self.runtime_gateway = runtime_gateway

  def create_task_from_function(self, function_passed, python_path):
    self.pickled = codecs.encode(cloudpickle.dumps(function_passed), "base64")

    script_function = "import pickle"
    script_function += "\n"
    script_function += "import codecs"
    script_function += "\n"
    script_function += "unpickled = pickle.loads(codecs.decode(%s, \"base64\"))" % self.pickled
    script_function += "\n"
    script_function += "print(unpickled())"

    python_script = self.runtime_gateway.jvm.org.ow2.proactive.scripting.SimpleScript(script_function, "cpython")
    task_script = self.runtime_gateway.jvm.org.ow2.proactive.scripting.TaskScript(python_script)
    script_task = self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.ScriptTask()
    script_task.setScript(task_script)
    script_task.addGenericInformation("PYTHON_COMMAND", python_path)

    job = self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.job.TaskFlowJob()
    job.setName("Python Lambda")

    script_task.setName("Python_Lambda")
    job.addTask(script_task)
    job.setInputSpace("")
    job.setOutputSpace("")
    print(job.display())

    return job

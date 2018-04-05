import os
import cloudpickle
import codecs

from .ScriptLanguage import *


class SerialisationHelper:
  """
  Simple client for the ProActive scheduler REST API
  See also https://try.activeeon.com/rest/doc/jaxrsdocs/overview-summary.html
  """
  runtime_gateway = None
  script_language = None

  def __init__(self, runtime_gateway):
    self.runtime_gateway = runtime_gateway
    self.script_language = ScriptLanguage()

  def create_simple_script(self, script_code, script_language):
    return self.runtime_gateway.jvm.org.ow2.proactive.scripting.SimpleScript(script_code, script_language)

  def create_task_script(self, simple_script):
    return self.runtime_gateway.jvm.org.ow2.proactive.scripting.TaskScript(simple_script)

  def create_script_task(self):
    return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.task.ScriptTask()

  def create_job(self):
    return self.runtime_gateway.jvm.org.ow2.proactive.scheduler.common.job.TaskFlowJob()

  def create_python_task_from_file(self, file_python, script_params={}):
    script_python = ''
    if os.path.exists(file_python):
      with open(file_python, 'r') as content_file:
        script_python = content_file.read()
    return self.create_python_task_from_script(script_python, script_params)

  def create_python_task_from_script(self, script_python, script_params={}):
    python_script = self.create_simple_script(script_python, self.script_language.python())
    task_script = self.create_task_script(python_script)
    script_task = self.create_script_task()

    if 'TASK_NAME' in script_params:
      script_task.setName(script_params["TASK_NAME"])
    else:
      script_task.setName("Python_Task")
    script_task.setScript(task_script)

    if 'PYTHON_COMMAND' in script_params:
      script_task.addGenericInformation("PYTHON_COMMAND", script_params["PYTHON_COMMAND"])

    job = self.create_job()
    if 'JOB_NAME' in script_params:
      job.setName(script_params["JOB_NAME"])
    else:
      job.setName("Python_Job")

    job.addTask(script_task)
    job.setInputSpace("")
    job.setOutputSpace("")

    if 'JOB_DISPLAY' in script_params and script_params["JOB_DISPLAY"] == True:
      print(job.display())

    return job

  def create_python_task_from_function(self, function_passed, python_path=None):
    pickled = codecs.encode(cloudpickle.dumps(function_passed), "base64")

    script_function = "import pickle"
    script_function += "\n"
    script_function += "import codecs"
    script_function += "\n"
    script_function += "unpickled = pickle.loads(codecs.decode(%s, \"base64\"))" % pickled
    script_function += "\n"
    script_function += "print(unpickled())"

    script_params = {
      'TASK_NAME': 'Python_Lambda',
      'JOB_NAME':  'Python Lambda',
      'JOB_DISPLAY': True
    }

    if python_path is not None:
      script_params['PYTHON_COMMAND'] = python_path

    return self.create_python_task_from_script(script_function, script_params)

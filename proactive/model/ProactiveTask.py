import os
import cloudpickle
import codecs

from .ProactiveScriptLanguage import *
from .ProactiveSelectionScript import *



class ProactiveTask:
  """
  Represent a generic proactive task

  script_language (ProactiveScriptLanguage)
  script_code (string)
  task_name (string)
  generic_information (map)
  """
  script_language = None
  task_name = ''
  task_implementation = ''
  generic_information = {}
  selection_script = None

  def __init__(self, script_language):
    self.setScriptLanguage(script_language)

  def setScriptLanguage(self, script_language):
    self.script_language = script_language

  def getScriptLanguage(self):
    return self.script_language

  def setSelectionScript(self, selection_script):
    self.selection_script = selection_script

  def getSelectionScript(self):
    return self.selection_script

  def setTaskName(self, task_name):
    self.task_name = task_name

  def getTaskName(self):
    return self.task_name

  def setTaskImplementationFromFile(self, task_file):
    if os.path.exists(task_file):
      with open(task_file, 'r') as content_file:
        self.task_implementation = content_file.read()

  def setTaskImplementationFromLambdaFunction(self, lambda_function):
    pickled_lambda = codecs.encode(cloudpickle.dumps(lambda_function), "base64")

    task_implementation = "import pickle"
    task_implementation += "\n"
    task_implementation += "import codecs"
    task_implementation += "\n"
    task_implementation += "result = pickle.loads(codecs.decode(%s, \"base64\"))()" % pickled_lambda

    self.setTaskImplementation(task_implementation)

  def setTaskImplementation(self, task_implementation):
    self.task_implementation = task_implementation

  def getTaskImplementation(self):
    return self.task_implementation

  def addGenericInformation(self, key, value):
    self.generic_information[key] = value

  def getGenericInformation(self):
    return self.generic_information


class ProactivePythonTask(ProactiveTask):
  """
    Represent a proactive python task
  """
  def __init__(self):
    super().__init__(ProactiveScriptLanguage().python())

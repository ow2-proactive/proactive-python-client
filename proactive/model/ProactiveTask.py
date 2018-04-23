import os
import cloudpickle
import codecs

from .ProactiveScriptLanguage import *
from .ProactiveSelectionScript import *


class ProactiveTask:
  """
  Represent a generic proactive task

  script_language (ProactiveScriptLanguage)
  fork_environment (ProactiveForkEnv)
  task_name (string)
  task_implementation (string)
  generic_information (map)
  """
  script_language = None
  fork_environment = None
  selection_script = None
  task_name = ''
  task_implementation = ''
  generic_information = {}

  def __init__(self, script_language = None):
    self.script_language = script_language
    self.fork_environment = None
    self.selection_script = None
    self.task_name = ''
    self.task_implementation = ''
    self.generic_information = {}

  def setScriptLanguage(self, script_language):
    self.script_language = script_language

  def getScriptLanguage(self):
    return self.script_language

  def setForkEnvironment(self, fork_environment):
    self.fork_environment = fork_environment

  def getForkEnvironment(self):
    return self.fork_environment

  def hasForkEnvironment(self):
    if self.fork_environment is not None:
      return True
    else:
      return False

  def setSelectionScript(self, selection_script):
    self.selection_script = selection_script

  def getSelectionScript(self):
    return self.selection_script

  def hasSelectionScript(self):
    if self.selection_script is not None:
      return True
    else:
      return False

  def setTaskName(self, task_name):
    self.task_name = task_name

  def getTaskName(self):
    return self.task_name

  def setTaskImplementationFromFile(self, task_file):
    if os.path.exists(task_file):
      task_implementation = "import subprocess"
      task_implementation += "\n"
      task_implementation += "result = subprocess.check_output('python %s' % '"+task_file+"', shell=True).strip()"
      self.setTaskImplementation(task_implementation)
    

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


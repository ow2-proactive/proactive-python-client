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
  input_files (list)
  output_files (list)
  """
  script_language = None
  fork_environment = None
  selection_script = None
  task_name = ''
  task_implementation = ''
  generic_information = {}
  input_files = []
  output_files = []

  def __init__(self, script_language=None):
    self.script_language = script_language
    self.fork_environment = None
    self.selection_script = None
    self.task_name = ''
    self.task_implementation = ''
    self.generic_information = {}
    self.input_files = []
    self.output_files = []

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

  def setTaskImplementationFromFile(self, task_file, parameters=[], displayTaskResultOnScheduler=True):
    if os.path.exists(task_file):
      params_string = ' '.join(parameters)
      task_implementation = "import subprocess"
      task_implementation += "\n"
      task_implementation += "print('Running " + task_file + " with " + params_string + " as parameters...')"
      task_implementation += "\n"
      task_implementation += "result = subprocess.check_output('python " + task_file + " " + params_string + "', shell=True).strip()"
      task_implementation += "\n"
      if displayTaskResultOnScheduler:
        task_implementation += "print('---')"
        task_implementation += "\n"
        task_implementation += "print(result.decode('ascii'))"
        task_implementation += "\n"
        task_implementation += "print('---')"
        task_implementation += "\n"
      task_implementation += "print('Finished')"
      self.setTaskImplementation(task_implementation)
      self.addInputFile(task_file)

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

  def addInputFile(self, input_file):
    self.input_files.append(input_file)

  def getInputFiles(self):
    return self.input_files

  def addOutputFile(self, output_file):
    self.output_files.append(output_file)

  def getOutputFiles(self):
    return self.output_files


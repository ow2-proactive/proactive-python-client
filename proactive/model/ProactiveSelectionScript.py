import os
import cloudpickle
import codecs

from .ProactiveScriptLanguage import *


class ProactiveSelectionScript:
  """
  Represent a proactive selection script

  script_language (ProactiveScriptLanguage)
  script_code (string)
  """
  script_language = None
  implementation = ''
  is_dynamic = True


  def __init__(self, script_language):
    self.setScriptLanguage(script_language)

  def setScriptLanguage(self, script_language):
    self.script_language = script_language

  def getScriptLanguage(self):
    return self.script_language
  
  def setIsDynamic(self, is_dynamic):
    self.is_dynamic = is_dynamic

  def isDynamic(self):
    return self.is_dynamic


  def setImplementationFromFile(self, task_file):
    if os.path.exists(task_file):
      with open(task_file, 'r') as content_file:
        self.implementation = content_file.read()

  def setImplementationFromLambdaFunction(self, lambda_function):
    pickled_lambda = codecs.encode(cloudpickle.dumps(lambda_function), "base64")

    implementation = "import pickle"
    implementation += "\n"
    implementation += "import codecs"
    implementation += "\n"
    implementation += "selected = pickle.loads(codecs.decode(%s, \"base64\"))()" % pickled_lambda

    self.setImplementation(implementation)

  def setImplementation(self, implementation):
    self.implementation = implementation

  def getImplementation(self):
    return self.implementation

class ProactivePythonSelectionScript(ProactiveSelectionScript):
  """
    Represent a proactive python selection script
  """
  def __init__(self):
    super().__init__(ProactiveScriptLanguage().python())
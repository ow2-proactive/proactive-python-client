import os


class ProactiveForkEnv:
  """
  Represent a generic proactive fork env

  script_language (ProactiveScriptLanguage)
  task_name (string)
  generic_information (map)
  """
  script_language = None
  task_implementation = ''
  java_home = '/usr'

  def __init__(self, script_language = None):
    self.script_language = script_language
    self.task_implementation = ''
    self.java_home = '/usr'

  def setScriptLanguage(self, script_language):
    self.script_language = script_language

  def getScriptLanguage(self):
    return self.script_language

  def setImplementation(self, task_implementation):
    self.task_implementation = task_implementation

  def getImplementation(self):
    return self.task_implementation

  def setImplementationFromFile(self, task_file):
    if os.path.exists(task_file):
      with open(task_file, 'r') as content_file:
        self.task_implementation = content_file.read()

  def setJavaHome(self, java_home):
    self.java_home = java_home

  def getJavaHome(self):
    return self.java_home


import os


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
    self.script_language = script_language
    self.implementation = ''
    self.is_dynamic = True

  def setScriptLanguage(self, script_language):
    self.script_language = script_language

  def getScriptLanguage(self):
    return self.script_language
  
  def setIsDynamic(self, is_dynamic):
    self.is_dynamic = is_dynamic

  def isDynamic(self):
    return self.is_dynamic

  def setImplementation(self, implementation):
    self.implementation = implementation

  def getImplementation(self):
    return self.implementation

  def setImplementationFromFile(self, task_file):
    if os.path.exists(task_file):
      with open(task_file, 'r') as content_file:
        self.implementation = content_file.read()


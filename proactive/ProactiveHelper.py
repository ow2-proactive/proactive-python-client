from .ProactiveScriptLanguage import *
from .ProactiveFactory import *
from .ProactiveTask import *
from .ProactiveJob import *
from .ProactiveBuilder import *


class ProactiveHelper:
  """
    Proactive helper for creating tasks and jobs

    proactive_factory (ProactiveFactory)
    script_language (ProactiveScriptLanguage)
  """
  proactive_factory = None
  script_language = None

  def __init__(self, runtime_gateway):
    self.proactive_factory = ProactiveFactory(runtime_gateway)
    self.script_language = ProactiveScriptLanguage()

  def createTask(self):
    return ProactiveTask()

  def createPythonTask(self):
    return ProactivePythonTask()

  def createJob(self):
    return ProactiveJob()

  def buildJob(self, job):
    return ProactiveJobBuilder(self.proactive_factory, job).create()


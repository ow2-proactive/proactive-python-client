from .ProactiveTask import *
from .ProactiveJob import *


class ProactiveBuilder:
  """
    Represent a generic builder

    proactive_factory (ProactiveFactory)
  """
  proactive_factory = None

  def __init__(self, proactive_factory):
    self.setProactiveFactory(proactive_factory)

  def setProactiveFactory(self, proactive_factory):
    self.proactive_factory = proactive_factory

  def getProactiveFactory(self):
    return self.proactive_factory


class ProactiveTaskBuilder(ProactiveBuilder):
  """
    Represent a proactive task builder

    proactive_task (ProactiveTask)
    script (jvm.org.ow2.proactive.scripting.SimpleScript)
    task_script (jvm.org.ow2.proactive.scripting.TaskScript)
    script_task (jvm.org.ow2.proactive.scheduler.common.task.ScriptTask)
  """
  proactive_task = ProactiveTask(None)
  script = None
  task_script = None
  script_task = None

  def __init__(self, proactive_factory, proactive_task):
    super().__init__(proactive_factory)
    self.setProactiveTask(proactive_task)

  def setProactiveTask(self, proactive_task):
    self.proactive_task = proactive_task

  def getProactiveTask(self):
    return self.proactive_task

  def __createScript__(self):
    assert self.proactive_task.getScriptLanguage() is not None

    self.script = self.proactive_factory.create_simple_script(
      self.proactive_task.getTaskImplementation(),
      self.proactive_task.getScriptLanguage()
    )
    return self.script

  def __createTaskScript__(self, script):
    self.task_script = self.proactive_factory.create_task_script(script)
    return self.task_script

  def __createScriptTask__(self, task_script):
    self.script_task = self.proactive_factory.create_script_task()
    self.script_task.setName(self.proactive_task.getTaskName())
    self.script_task.setScript(task_script)

    for key, value in self.proactive_task.getGenericInformation().items():
      self.script_task.addGenericInformation(key, value)

    return self.script_task

  def create(self):
    return self.__createScriptTask__(
      self.__createTaskScript__(
        self.__createScript__()
      )
    )


class ProactiveJobBuilder:
  """
    Represent a proactive job builder

    proactive_factory (ProactiveFactory)
    proactive_job (ProactiveJob)
    job (jvm.org.ow2.proactive.scheduler.common.job.TaskFlowJob)
  """
  proactive_factory = None
  proactive_job = ProactiveJob()
  job = None

  def __init__(self, proactive_factory, proactive_job):
    self.setProactiveFactory(proactive_factory)
    self.setProactiveJob(proactive_job)

  def setProactiveFactory(self, proactive_factory):
    self.proactive_factory = proactive_factory

  def getProactiveFactory(self):
    return self.proactive_factory

  def setProactiveJob(self, proactive_job):
    self.proactive_job = proactive_job

  def getProactiveJob(self):
    return self.proactive_job

  def create(self, debug=False):
    self.job = self.proactive_factory.create_job()
    self.job.setName(self.proactive_job.getJobName())

    for task in self.proactive_job.getTasks():
      self.job.addTask(ProactiveTaskBuilder(self.proactive_factory, task).create())

    self.job.setInputSpace("")
    self.job.setOutputSpace("")

    if debug:
      print(self.job.display())

    return self.job

from .model.ProactiveTask import *
from .model.ProactiveJob import *

#__metaclass__ = type
class ProactiveBuilder(object):
    """
      Represent a generic builder

      proactive_factory (ProactiveFactory)
    """

    def __init__(self, proactive_factory=None):
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

    def __init__(self, proactive_factory, proactive_task_model=None):
        super(ProactiveTaskBuilder, self).__init__(proactive_factory)
        self.setProactiveTaskModel(proactive_task_model)

    def setProactiveTaskModel(self, proactive_task_model):
        self.proactive_task_model = proactive_task_model

    def getProactiveTaskModel(self):
        return self.proactive_task_model

    def __create_script__(self):
        assert self.proactive_task_model.getScriptLanguage() is not None

        self.script = self.proactive_factory.create_simple_script(
            self.proactive_task_model.getTaskImplementation(),
            self.proactive_task_model.getScriptLanguage()
        )
        return self.script

    def __create_task_script__(self, script):
        self.task_script = self.proactive_factory.create_task_script(script)
        return self.task_script

    def __create_fork_environment__(self, fork_environment):
        simple_script = self.proactive_factory.create_simple_script(
            fork_environment.getImplementation(),
            fork_environment.getScriptLanguage()
        )

        fork_env = self.proactive_factory.create_fork_environment()
        fork_env.setEnvScript(simple_script)
        fork_env.setJavaHome(fork_environment.getJavaHome())

        return fork_env

    def __create_selection_script__(self, selection_script):
        return self.proactive_factory.create_selection_script(
            selection_script.getImplementation(),
            selection_script.getScriptLanguage(),
            selection_script.isDynamic()
        )

    def __create_pre_script__(self, pre_script):
        return self.proactive_factory.create_simple_script(
                    pre_script.getImplementation(),
                    pre_script.getScriptLanguage()
                )

    def __create_post_script__(self, post_script):
        return self.proactive_factory.create_simple_script(
                    post_script.getImplementation(),
                    post_script.getScriptLanguage()
                )

    def __create_script_task__(self, task_script):
        self.script_task = self.proactive_factory.create_script_task()
        self.script_task.setName(self.proactive_task_model.getTaskName())
        self.script_task.setScript(task_script)

        if self.proactive_task_model.hasForkEnvironment():
            self.script_task.setForkEnvironment(
                self.__create_fork_environment__(
                    self.proactive_task_model.getForkEnvironment()
                )
            )

        if self.proactive_task_model.hasSelectionScript():
            self.script_task.setSelectionScript(
                self.__create_selection_script__(
                    self.proactive_task_model.getSelectionScript()
                )
            )

        if self.proactive_task_model.hasPreScript():
            self.script_task.setPreScript(
                self.__create_pre_script__(self.proactive_task_model.getPreScript())
            )

        if self.proactive_task_model.hasPostScript():
            self.script_task.setPostScript(
                self.__create_post_script__(self.proactive_task_model.getPostScript())
            )

        for key, value in self.proactive_task_model.getGenericInformation().items():
            self.script_task.addGenericInformation(key, value)

        InputAccessMode = self.proactive_factory.get_input_access_mode()
        transferFromInputSpace = InputAccessMode.getAccessMode("transferFromInputSpace")
        print("Input Files to transfer: ", len(self.proactive_task_model.getInputFiles()))
        for file in self.proactive_task_model.getInputFiles():
            self.script_task.addInputFiles(file, transferFromInputSpace)


        OutputAccessMode = self.proactive_factory.get_output_access_mode()
        transferToOutputSpace = OutputAccessMode.getAccessMode("transferToOutputSpace")
        print("Output Files to transfer: ", len(self.proactive_task_model.getOutputFiles()))
        for file in self.proactive_task_model.getOutputFiles():
            self.script_task.addOutputFiles(file, transferToOutputSpace)

        return self.script_task

    def create(self):
        return self.__create_script_task__(
            self.__create_task_script__(
                self.__create_script__()
            )
        )


class ProactiveJobBuilder(ProactiveBuilder):
    """
      Represent a proactive job builder

      proactive_factory (ProactiveFactory)
      proactive_job (ProactiveJob)
      job (org.ow2.proactive.scheduler.common.job.TaskFlowJob)
    """

    def __init__(self, proactive_factory, proactive_job_model=None):
        super(ProactiveJobBuilder, self).__init__(proactive_factory)
        self.setProactiveJobModel(proactive_job_model)

    def setProactiveFactory(self, proactive_factory):
        self.proactive_factory = proactive_factory

    def getProactiveFactory(self):
        return self.proactive_factory

    def setProactiveJobModel(self, proactive_job):
        self.proactive_job_model = proactive_job

    def getProactiveJobModel(self):
        return self.proactive_job_model

    def getProactiveJob(self):
        return self.proactive_job

    def create(self):
        self.proactive_job = self.proactive_factory.create_job()
        self.proactive_job.setName(self.proactive_job_model.getJobName())

        #proactive_task_list = []
        proactive_task_map = {}
        for proactive_task_model in self.proactive_job_model.getTasks():
            print("Adding task ", proactive_task_model.getTaskName(), " to the job ", self.proactive_job.getName())
            proactive_task = ProactiveTaskBuilder(self.proactive_factory, proactive_task_model).create()
            self.proactive_job.addTask(proactive_task)
            #proactive_task_list.append(proactive_task)
            proactive_task_map[proactive_task_model.getTaskName()] = [proactive_task_model, proactive_task]

        #for proactive_task in proactive_task_list:
        for task_name in proactive_task_map:
            proactive_task_model, proactive_task = proactive_task_map[task_name]
            #task = proactive_task.getProactiveTaskModel()
            for dependency_task_model in proactive_task_model.getDependencies():
                print("Adding task ", dependency_task_model.getTaskName(), " as a dependency of ", proactive_task_model.getTaskName())
                _, proactive_dependency_task = proactive_task_map[dependency_task_model.getTaskName()]
                proactive_task.addDependence(proactive_dependency_task)

        #self.proactive_job.setInputSpace(self.proactive_job_model.getInputFolder())
        #self.proactive_job.setOutputSpace(self.proactive_job_model.getOutputFolder())

        return self

    def toString(self):
        if self.getProactiveJob() is not None:
            return self.getProactiveJob().display()

    def display(self, enabled=False):
        if enabled:
            print(self.toString())
        return self


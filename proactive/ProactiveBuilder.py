from py4j.java_collections import MapConverter

from .model.ProactiveTask import *
from .model.ProactiveJob import *
import logging
import logging.config


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

    def __init__(self, proactive_factory, proactive_task_model=None, debug=False, log4py_props_file=None):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        super(ProactiveTaskBuilder, self).__init__(proactive_factory)
        self.setProactiveTaskModel(proactive_task_model)
        self.debug = debug
        self.log4py_props_file = log4py_props_file
        if self.debug:
            if log4py_props_file is None:
                self.log4py_props_file = os.path.join(self.root_dir, 'logging.conf')
            logging.config.fileConfig(self.log4py_props_file)
        self.logger = logging.getLogger('ProactiveBuilder')

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

    def __create_flow_script__(self, _flow_script):
        if _flow_script.isReplicateFlowScript():
            self.logger.debug('Building a replicate flow script')
            flow_script = self.__create_replicate_flow_script_(_flow_script)
        elif _flow_script.isLoopFlowScript():
            self.logger.debug('Building a loop flow script')
            flow_script = self.__create_loop_flow_script_(_flow_script)
        elif _flow_script.isBranchFlowScript():
            self.logger.debug('Building a branch flow script')
            flow_script = self.__create_branch_flow_script_(_flow_script)
        else:
            flow_script = None
        return flow_script

    def __create_replicate_flow_script_(self, _flow_script):
        flow_script = self.__get_flow_script__().createReplicateFlowScript(_flow_script.getImplementation(),
                                                                           _flow_script.getScriptLanguage())
        return flow_script

    def __create_loop_flow_script_(self, _flow_script):
        flow_script = self.__get_flow_script__().createLoopFlowScript(_flow_script.getImplementation(),
                                                                      _flow_script.getScriptLanguage(),
                                                                      _flow_script.getActionTarget())
        return flow_script

    def __create_branch_flow_script_(self, _flow_script):
        flow_script = self.__get_flow_script__().createIfFlowScript(_flow_script.getImplementation(),
                                                                    _flow_script.getScriptLanguage(),
                                                                    _flow_script.getActionTarget(),
                                                                    _flow_script.getActionTargetElse(),
                                                                    _flow_script.getActionTargetContinuation())
        return flow_script

    def __get_flow_script__(self):
        return self.proactive_factory.get_flow_script()

    def __get_flow_block__(self):
        return self.proactive_factory.get_flow_block()

    def __create_flow_block__(self, _flow_block):
        return self.__get_flow_block__().parse(_flow_block)

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
        self.logger.debug('Building and setting the script task')
        self.script_task = self.proactive_factory.create_script_task()
        self.script_task.setName(self.proactive_task_model.getTaskName())
        self.script_task.setScript(task_script)

        if self.proactive_task_model.hasForkEnvironment():
            self.logger.debug('Building and setting the fork environment')
            self.script_task.setForkEnvironment(
                self.__create_fork_environment__(
                    self.proactive_task_model.getForkEnvironment()
                )
            )

        if self.proactive_task_model.hasSelectionScript():
            self.logger.debug('Building and setting the selection script')
            self.script_task.setSelectionScript(
                self.__create_selection_script__(
                    self.proactive_task_model.getSelectionScript()
                )
            )

        if self.proactive_task_model.hasFlowScript():
            self.logger.debug('Building and setting the flow script')
            self.script_task.setFlowScript(
                self.__create_flow_script__(
                    self.proactive_task_model.getFlowScript()
                )
            )

        if self.proactive_task_model.hasFlowBlock():
            self.logger.debug('Building and setting the flow block')
            self.script_task.setFlowBlock(
                self.__create_flow_block__(
                    self.proactive_task_model.getFlowBlock()
                )
            )

        if self.proactive_task_model.hasPreScript():
            self.logger.debug('Building and setting the pre script')
            self.script_task.setPreScript(
                self.__create_pre_script__(self.proactive_task_model.getPreScript())
            )

        if self.proactive_task_model.hasPostScript():
            self.logger.debug('Building and setting the post script')
            self.script_task.setPostScript(
                self.__create_post_script__(self.proactive_task_model.getPostScript())
            )

        if self.proactive_task_model.hasVariables():
            self.logger.debug('Adding variables')
            variables = {}
            for key, value in self.proactive_task_model.getVariables().items():
                task_var = self.proactive_factory.create_task_variable()
                task_var.setName(key)
                task_var.setValue(value)
                variables[key] = task_var
            javamap = MapConverter().convert(variables, self.proactive_factory.getRuntimeGateway()._gateway_client)
            self.script_task.setVariables(javamap)

        self.logger.debug('Adding the generic information')
        for key, value in self.proactive_task_model.getGenericInformation().items():
            self.script_task.addGenericInformation(key, value)

        InputAccessMode = self.proactive_factory.get_input_access_mode()
        transferFromInputSpace = InputAccessMode.getAccessMode("transferFromInputSpace")
        self.logger.info("Input Files to transfer: " + str(len(self.proactive_task_model.getInputFiles())))
        for file in self.proactive_task_model.getInputFiles():
            self.script_task.addInputFiles(file, transferFromInputSpace)


        OutputAccessMode = self.proactive_factory.get_output_access_mode()
        transferToOutputSpace = OutputAccessMode.getAccessMode("transferToOutputSpace")
        self.logger.info("Output Files to transfer: " + str(len(self.proactive_task_model.getOutputFiles())))
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

    def __init__(self, proactive_factory, proactive_job_model=None, debug=False, log4py_props_file=None):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        super(ProactiveJobBuilder, self).__init__(proactive_factory)
        self.setProactiveJobModel(proactive_job_model)
        self.debug = debug
        self.log4py_props_file = log4py_props_file
        if self.debug:
            if log4py_props_file is None:
                self.log4py_props_file = os.path.join(self.root_dir, 'logging.conf')
            logging.config.fileConfig(self.log4py_props_file)
        self.logger = logging.getLogger('ProactiveBuilder')

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
        self.logger.debug('Building the job')
        self.proactive_job = self.proactive_factory.create_job()
        self.proactive_job.setName(self.proactive_job_model.getJobName())

        #proactive_task_list = []
        proactive_task_map = {}
        self.logger.debug('Building tasks and adding them to the job')
        for proactive_task_model in self.proactive_job_model.getTasks():
            self.logger.info("Adding task " + proactive_task_model.getTaskName() + " to the job " + self.proactive_job.getName())
            proactive_task = ProactiveTaskBuilder(self.proactive_factory, proactive_task_model, self.debug, self.log4py_props_file).create()
            self.proactive_job.addTask(proactive_task)
            #proactive_task_list.append(proactive_task)
            proactive_task_map[proactive_task_model.getTaskName()] = [proactive_task_model, proactive_task]

        if self.proactive_job_model.hasVariables():
            self.logger.debug('Adding variables')
            variables = {}
            for key, value in self.proactive_job_model.getVariables().items():
                task_var = self.proactive_factory.create_job_variable()
                task_var.setName(key)
                task_var.setValue(value)
                variables[key] = task_var
            javamap = MapConverter().convert(variables, self.proactive_factory.getRuntimeGateway()._gateway_client)
            self.proactive_job.setVariables(javamap)

        self.logger.debug('Adding the generic information')
        for key, value in self.proactive_job_model.getGenericInformation().items():
            self.proactive_job.addGenericInformation(key, value)

        self.logger.debug('Adding dependencies to the tasks')
        #for proactive_task in proactive_task_list:
        for task_name in proactive_task_map:
            proactive_task_model, proactive_task = proactive_task_map[task_name]
            #task = proactive_task.getProactiveTaskModel()
            for dependency_task_model in proactive_task_model.getDependencies():
                self.logger.info("Adding task " + dependency_task_model.getTaskName() + " as a dependency of " + proactive_task_model.getTaskName())
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

import proactive
import unittest
import numbers
import os
import pytest


class GatewayTestSuite(unittest.TestCase):
    """Advanced test cases."""

    gateway = None
    username = ""
    password = ""

    @pytest.fixture(autouse=True)
    def setup_gateway(self, metadata):
        self.gateway = proactive.ProActiveGateway(metadata['proactive_url'], debug=True)
        self.username = metadata['username']
        self.password = metadata['password']

    def test_submit_workflow_from_catalog(self):
        self.gateway.connect(self.username, self.password)
        jobId = self.gateway.submitWorkflowFromCatalog("basic-examples", "Print_File_Name")
        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_workflow_from_catalog_with_variables(self):
        self.gateway.connect(self.username, self.password)
        jobId = self.gateway.submitWorkflowFromCatalog("basic-examples", "Print_File_Name", {'file': 'test_submit_from_catalog_with_variables'})
        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_workflow_from_catalog_with_generic_info(self):
        self.gateway.connect(self.username, self.password)
        jobId = self.gateway.submitWorkflowFromCatalog("basic-examples", "Print_File_Name", {}, {'GI': 'test'})
        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_workflow_from_file(self):
        self.gateway.connect(self.username, self.password)
        workflow_file_path = os.getcwd() + '/tests/print_file_name.xml'
        jobId = self.gateway.submitWorkflowFromFile(workflow_file_path)
        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_workflow_from_file_with_variables(self):
        self.gateway.connect(self.username, self.password)
        workflow_file_path = os.getcwd() + '/tests/print_file_name.xml'
        jobId = self.gateway.submitWorkflowFromFile(workflow_file_path, {'file': 'test_submit_file_with_variables'})
        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_python_script_from_file_with_precious_result(self):
        self.gateway.connect(self.username, self.password)

        pythonTask = self.gateway.createPythonTask()
        pythonTask.setTaskName("PythonTaskFromFileWithPreciousResult")
        pythonTask.setTaskImplementation("""print("Hello world!")""")
        pythonTask.setPreciousResult(True)

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithPreciousResult")
        myJob.addTask(pythonTask)
        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    ## def test_submit_workflow_from_URL(self):
    #     self.gateway.connect(self.username, self.password)
    #     workflow_url = 'https://raw.githubusercontent.com/ow2-proactive/proactive-python-client/master/tests/print_file_name.xml'
    #     jobId = self.gateway.submitWorkflowFromURL(workflow_url, {'file': 'test_submit_URL'})
    #     self.assertIsNotNone(jobId)
    #     self.assertTrue(isinstance(jobId, numbers.Number))
    #     self.gateway.disconnect()

    ## def test_submit_python_lambda(self):
    #     self.gateway.connect(self.username, self.password)
    #
    #     pythonTask = self.gateway.createPythonTask()
    #     pythonTask.setTaskName("SimplePythonLambdaTask")
    #     pythonTask.setTaskExecutionFromLambdaFunction(lambda: 88 - 20 * 10)
    #     #pythonTask.setTaskImplementationFromLambdaFunction(lambda: 88 - 20 * 10)
    #     #pythonTask.addGenericInformation("PYTHON_COMMAND", "/usr/bin/python3")
    #     #script_forkenv = os.getcwd() + '/scripts/fork_env.py'
    #     #forkEnv = self.gateway.createDefaultForkEnvironment()
    #     #forkEnv.setImplementationFromFile(script_forkenv)
    #     #pythonTask.setForkEnvironment(forkEnv)
    #
    #     myJob = self.gateway.createJob()
    #     myJob.setJobName("SimplePythonLambdaJob")
    #     myJob.addTask(pythonTask)
    #     jobId = self.gateway.submitJob(myJob)
    #
    #     self.assertIsNotNone(jobId)
    #     self.assertTrue(isinstance(jobId, numbers.Number))
    #     self.gateway.disconnect()

    def test_submit_python_script(self):
        self.gateway.connect(self.username, self.password)

        pythonTask = self.gateway.createPythonTask()
        pythonTask.setTaskName("SimplePythonTask")
        pythonTask.setTaskImplementation("""print("Hello world!")""")

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJob")
        myJob.addTask(pythonTask)
        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_python_script_with_replicate(self):
        self.gateway.connect(self.username, self.password)

        # Creating the split task
        pythonTaskSplit = self.gateway.createPythonTask()
        pythonTaskSplit.setTaskName("SplitPythonTask")
        pythonTaskSplit.setTaskImplementation("""print("Hello world!")""")

        pythonTaskSplit.setFlowBlock(self.gateway.getProactiveFlowBlockType().start())

        replicateScript = "runs = 1"
        flow_script = self.gateway.createReplicateFlowScript(replicateScript)
        pythonTaskSplit.setFlowScript(flow_script)

        # Creating the replicated task
        pythonTaskProcess = self.gateway.createPythonTask()
        pythonTaskProcess.setTaskName("ReplicatedPythonTask")
        pythonTaskProcess.setTaskImplementation("""print("Hello world!")""")
        pythonTaskProcess.addDependency(pythonTaskSplit)

        # Creating the merging task
        pythonTaskMerge = self.gateway.createPythonTask()
        pythonTaskMerge.setTaskName("MergePythonTask")
        pythonTaskMerge.setTaskImplementation("""print("Hello world!")""")

        pythonTaskMerge.setFlowBlock(self.gateway.getProactiveFlowBlockType().end())
        pythonTaskMerge.addDependency(pythonTaskProcess)

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithReplicatedTask")

        myJob.addTask(pythonTaskSplit)
        myJob.addTask(pythonTaskProcess)
        myJob.addTask(pythonTaskMerge)

        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_python_script_with_loop(self):
        self.gateway.connect(self.username, self.password)

        # Creating the start task
        pythonTaskStart = self.gateway.createPythonTask()
        pythonTaskStart.setTaskName("StartPythonTask")
        pythonTaskStart.setTaskImplementation("""print("Hello world!")""")

        pythonTaskStart.setFlowBlock(self.gateway.getProactiveFlowBlockType().start())

        # Creating the loop task
        pythonTaskLoop = self.gateway.createPythonTask()
        pythonTaskLoop.setTaskName("LoopPythonTask")
        pythonTaskLoop.setTaskImplementation("""print("Hello world!")""")
        pythonTaskLoop.addDependency(pythonTaskStart)

        loopScript = """if(variables.get('PA_TASK_ITERATION') < 1) { loop = true; } else { loop = false; }"""
        flow_script = self.gateway.createLoopFlowScript(loopScript, pythonTaskStart.getTaskName())
        pythonTaskLoop.setFlowScript(flow_script)
        pythonTaskLoop.setFlowBlock(self.gateway.getProactiveFlowBlockType().end())

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithLoopTask")

        myJob.addTask(pythonTaskStart)
        myJob.addTask(pythonTaskLoop)

        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_python_script_with_branch(self):
        self.gateway.connect(self.username, self.password)

        # Creating the condition task
        pythonTaskCondition = self.gateway.createPythonTask()
        pythonTaskCondition.setTaskName("ConditionPythonTask")
        pythonTaskCondition.setTaskImplementation("""print("Hello condition world!")""")

        # Creating the If task
        pythonTaskIf = self.gateway.createPythonTask()
        pythonTaskIf.setTaskName("IfPythonTask")
        pythonTaskIf.setTaskImplementation("""print("If task.")""")

        # Creating the Else task
        pythonTaskElse = self.gateway.createPythonTask()
        pythonTaskElse.setTaskName("ElsePythonTask")
        pythonTaskElse.setTaskImplementation("""print("Else task should be skipped.")""")

        # Creating the Continuation task
        pythonTaskContinuation = self.gateway.createPythonTask()
        pythonTaskContinuation.setTaskName("ContinuationPythonTask")
        pythonTaskContinuation.setTaskImplementation("""print("Continuation task.")""")

        branchScript = """if(true){ branch = "if"; } else { branch = "else"; }"""

        flow_script = self.gateway.createBranchFlowScript(branchScript,
                                                          pythonTaskIf.getTaskName(),
                                                          pythonTaskElse.getTaskName(),
                                                          pythonTaskContinuation.getTaskName())
        pythonTaskCondition.setFlowScript(flow_script)

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithBranchTask")

        myJob.addTask(pythonTaskCondition)
        myJob.addTask(pythonTaskIf)
        myJob.addTask(pythonTaskElse)
        myJob.addTask(pythonTaskContinuation)

        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_python_script_with_dependencies(self):
        self.gateway.connect(self.username, self.password)

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithDependencies")

        pythonTask1 = self.gateway.createPythonTask()
        pythonTask1.setTaskName("SimplePythonTask1")
        pythonTask1.setTaskImplementation("""print("Hello world (1)!")""")
        myJob.addTask(pythonTask1)

        pythonTask2 = self.gateway.createPythonTask()
        pythonTask2.setTaskName("SimplePythonTask2")
        pythonTask2.setTaskImplementation("""print("Hello world (2)!")""")
        myJob.addTask(pythonTask2)

        pythonTask3 = self.gateway.createPythonTask()
        pythonTask3.setTaskName("SimplePythonTask3")
        pythonTask3.setTaskImplementation("""print("Hello world (3)!")""")
        pythonTask3.addDependency(pythonTask1)
        pythonTask3.addDependency(pythonTask2)
        myJob.addTask(pythonTask3)

        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_python_script_from_file(self):
        self.gateway.connect(self.username, self.password)

        pythonTask = self.gateway.createPythonTask()
        pythonTask.setTaskName("SimplePythonTaskFromFile")
        pythonTask.setTaskImplementationFromFile('scripts/print_python_env.py')

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobFromFile")
        myJob.addTask(pythonTask)
        myJob.setInputFolder(os.getcwd())
        myJob.setOutputFolder(os.getcwd())

        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))

        job_result = self.gateway.getJobResult(jobId)
        self.assertIsNotNone(job_result)

        self.gateway.disconnect()

    # def test_submit_python_script_from_file_execution(self):
    #     self.gateway.connect(self.username, self.password)

    #     pythonTask = self.gateway.createPythonTask()
    #     pythonTask.setTaskName("SimplePythonTaskFromFileExecution")
    #     pythonTask.setTaskExecutionFromFile('examples/demo_exec_file/main.py', ['param1', 'param2'])
    #     pythonTask.addInputFile('examples/demo_exec_file/hellopkg/__init__.py')
    #     pythonTask.addInputFile('examples/demo_exec_file/hellopkg/hello.py')

    #     myJob = self.gateway.createJob()
    #     myJob.setJobName("SimplePythonJobFromFileExecution")
    #     myJob.addTask(pythonTask)

    #     jobId = self.gateway.submitJobWithInputsAndOutputsPaths(myJob)

    #     self.assertIsNotNone(jobId)
    #     self.assertTrue(isinstance(jobId, numbers.Number))

    #     job_result = self.gateway.getJobResult(jobId)
    #     self.assertIsNotNone(job_result)

    #     self.gateway.disconnect()

    def test_get_job_info(self):
        self.gateway.connect(self.username, self.password)
        jobId = self.gateway.submitWorkflowFromCatalog("basic-examples", "Print_File_Name")
        job_info = self.gateway.getJobInfo(jobId)
        self.assertTrue(str(job_info.getJobId().value()) == str(jobId))
        self.assertTrue(str(job_info.getJobOwner()) == self.username)
        self.gateway.disconnect()

    def test_get_all_jobs(self):
        self.gateway.connect(self.username, self.password)
        jobId = self.gateway.submitWorkflowFromCatalog("basic-examples", "Print_File_Name")
        jobs = self.gateway.getAllJobs(my_jobs_only=True, pending=True, running=True, finished=True, withIssuesOnly=False, child_jobs=True,
                                       job_name=None, project_name=None, user_name=None, tenant=None, parent_id=None)
        self.assertTrue(jobs.size() > 0)
        for job_info in jobs:
            self.assertTrue(str(job_info.getJobOwner()) is not None)
            self.assertTrue(
                str(job_info.getStatus().name()) in ['FINISHED', 'KILLED', 'FAILED', 'IN_ERROR', 'CANCELED', 'PAUSED',
                                                     'FINISHED', 'STALLED', 'RUNNING', 'PENDING'])
        self.gateway.disconnect()

    def test_submit_python_script_from_file_with_fork_environment(self):
        self.gateway.connect(self.username, self.password)

        pythonTask = self.gateway.createPythonTask()
        pythonTask.setTaskName("PythonTaskFromFileWithForkEnv")
        pythonTask.setTaskImplementation("""print("Hello world!")""")

        script_forkenv = os.getcwd() + '/scripts/fork_env.groovy'
        fork_env = self.gateway.createForkEnvironment(language="groovy")
        fork_env.setImplementationFromFile(script_forkenv)
        pythonTask.setForkEnvironment(fork_env)

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithForkEnv")
        myJob.addTask(pythonTask)
        myJob.addVariable("CONTAINER_PLATFORM", "none")
        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_with_selection_script_groovy(self):
        self.gateway.connect(self.username, self.password)

        pythonTask = self.gateway.createPythonTask()
        pythonTask.setTaskName("PythonTaskWithSelectionScriptGroovy")
        pythonTask.setTaskImplementation("""print("Hello world!")""")

        selection_script = self.gateway.createSelectionScript(self.gateway.getProactiveScriptLanguage().groovy())
        selection_script.setImplementation("selected = true;")
        pythonTask.setSelectionScript(selection_script)

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithGroovySelectionScript")
        myJob.addTask(pythonTask)
        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_with_selection_script_groovy_from_file(self):
        self.gateway.connect(self.username, self.password)

        pythonTask = self.gateway.createPythonTask()
        pythonTask.setTaskName("PythonTaskWithSelectionScriptGroovy")
        pythonTask.setTaskImplementation("""print("Hello world!")""")

        script_selection_script = os.getcwd() + '/scripts/check_node_source_name.groovy'
        selection_script = self.gateway.createSelectionScript(language="groovy")
        selection_script.setImplementationFromFile(script_selection_script)
        pythonTask.setSelectionScript(selection_script)

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithGroovySelectionFromFile")
        myJob.addVariable("NODE_SOURCE_NAME", "On-Prem-Server-Static-Nodes")
        myJob.addTask(pythonTask)
        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_with_bash_script(self):
        self.gateway.connect(self.username, self.password)

        bashTask = self.gateway.createTask(self.gateway.getProactiveScriptLanguage().linux_bash())
        bashTask.setTaskName("BashTask")
        bashTask.setTaskImplementation("""pwd; ls -l; echo "This is a linux bash task";""")

        myJob = self.gateway.createJob()
        myJob.setJobName("SimpleBashJob")
        myJob.addTask(bashTask)
        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_python_script_with_pre_script(self):
        self.gateway.connect(self.username, self.password)

        pythonTask = self.gateway.createPythonTask()
        pythonTask.setTaskName("PythonTaskWithPreScript")
        pythonTask.setTaskImplementation("""print("Hello world from Python!")""")

        pre_script = self.gateway.createPreScript(self.gateway.getProactiveScriptLanguage().linux_bash())
        pre_script.setImplementation("""echo "This is a pre-script";""")
        pythonTask.setPreScript(pre_script)

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithPreScript")
        myJob.addTask(pythonTask)
        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_python_script_with_post_script(self):
        self.gateway.connect(self.username, self.password)

        pythonTask = self.gateway.createPythonTask()
        pythonTask.setTaskName("PythonTaskWithPostScript")
        pythonTask.setTaskImplementation("""print("Hello world from Python!")""")

        post_script = self.gateway.createPostScript(self.gateway.getProactiveScriptLanguage().linux_bash())
        post_script.setImplementation("""echo "This is a post-script";""")
        pythonTask.setPostScript(post_script)

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithPostScript")
        myJob.addTask(pythonTask)
        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()


if __name__ == '__main__':
    unittest.main()

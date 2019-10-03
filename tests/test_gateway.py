import proactive
import unittest
import numbers
import os
import pytest

#import requests
#from unittest.case import skip


class GatewayTestSuite(unittest.TestCase):
    """Advanced test cases."""

    gateway = None
    username = ""
    password = ""

    @pytest.fixture(autouse=True)
    def setup_gateway(self, metadata):
        self.gateway = proactive.ProActiveGateway(metadata['proactive_url'])
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
        jobId = self.gateway.submitWorkflowFromCatalog("basic-examples", "Print_File_Name",
                                                       {'file': 'test_submit_from_catalog_with_variables'})
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

    #def test_submit_workflow_from_URL(self):
    #  self.gateway.connect(self.username, self.password)
    #  workflow_url = 'https://raw.githubusercontent.com/ow2-proactive/proactive-python-client/master/tests/print_file_name.xml'
    #  jobId = self.gateway.submitWorkflowFromURL(workflow_url, {'file': 'test_submit_URL'})
    #  self.assertIsNotNone(jobId)
    #  self.assertTrue(isinstance(jobId, numbers.Number))
    #  self.gateway.disconnect()

    # def test_submit_python_lambda(self):
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

        replicateScript = "runs = 3"
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
        pythonTask.setTaskImplementationFromFile('scripts/hello.py')

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

    def test_submit_python_script_from_file_execution(self):
        self.gateway.connect(self.username, self.password)

        pythonTask = self.gateway.createPythonTask()
        pythonTask.setTaskName("SimplePythonTaskFromFileExecution")
        pythonTask.setTaskExecutionFromFile('main.py', ['param1', 'param2'])
        pythonTask.addInputFile('scripts/__init__.py')
        pythonTask.addInputFile('scripts/hello.py')

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobFromFileExecution")
        myJob.addTask(pythonTask)
        myJob.setInputFolder(os.getcwd())
        myJob.setOutputFolder(os.getcwd())

        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))

        job_result = self.gateway.getJobResult(jobId)
        self.assertIsNotNone(job_result)

        self.gateway.disconnect()

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
        jobs = self.gateway.getAllJobs()
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

        script_forkenv = os.getcwd() + '/scripts/fork_env.py'
        fork_env = self.gateway.createDefaultForkEnvironment()
        fork_env.setImplementationFromFile(script_forkenv)
        pythonTask.setForkEnvironment(fork_env)

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithForkEnv")
        myJob.addTask(pythonTask)
        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_python_script_from_file_with_selection_script(self):
        self.gateway.connect(self.username, self.password)

        pythonTask = self.gateway.createPythonTask()
        pythonTask.setTaskName("PythonTaskFromFileWithSelection")
        pythonTask.setTaskImplementation("""print("Hello world!")""")

        selection_script = self.gateway.createDefaultSelectionScript()
        selection_script.setImplementation("selected = True")
        pythonTask.setSelectionScript(selection_script)

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithSelection")
        myJob.addTask(pythonTask)
        jobId = self.gateway.submitJob(myJob)

        self.assertIsNotNone(jobId)
        self.assertTrue(isinstance(jobId, numbers.Number))
        self.gateway.disconnect()

    def test_submit_with_selection_script_groovy(self):
        self.gateway.connect(self.username, self.password)

        pythonTask = self.gateway.createPythonTask()
        pythonTask.setTaskName("PythonTaskFromFileWithSelectionGroovy")
        pythonTask.setTaskImplementation("""print("Hello world!")""")

        selection_script = self.gateway.createSelectionScript(self.gateway.getProactiveScriptLanguage().groovy())
        selection_script.setImplementation("selected = true;")
        pythonTask.setSelectionScript(selection_script)

        myJob = self.gateway.createJob()
        myJob.setJobName("SimplePythonJobWithGroovySelection")
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

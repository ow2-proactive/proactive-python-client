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
    jobId = self.gateway.submitWorkflowFromCatalog("basic-examples", "print_file_name")
    self.assertIsNotNone(jobId)
    self.assertTrue(isinstance(jobId, numbers.Number))
    self.gateway.disconnect()

  def test_submit_workflow_from_catalog_with_variables(self):
    self.gateway.connect(self.username, self.password)
    jobId = self.gateway.submitWorkflowFromCatalog("basic-examples", "print_file_name",
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

  def test_submit_workflow_from_URL(self):
    self.gateway.connect(self.username, self.password)
    workflow_url = 'https://gist.githubusercontent.com/marcocast/5b9df0478f9e093663eaae36ca2f55b0/raw/ad98492428243db5ebb812205488281b65189077/print_file_name.xml'
    jobId = self.gateway.submitWorkflowFromURL(workflow_url, {'file': 'test_submit_URL'})
    self.assertIsNotNone(jobId)
    self.assertTrue(isinstance(jobId, numbers.Number))
    self.gateway.disconnect()

  def test_submit_python_lambda(self):
    self.gateway.connect(self.username, self.password)

    pythonTask = self.gateway.createPythonTask()
    pythonTask.setTaskName("SimplePythonLambdaTask")
    pythonTask.setTaskImplementationFromLambdaFunction(lambda: 88 - 20 * 10)
    pythonTask.addGenericInformation("PYTHON_COMMAND", "/usr/bin/python3") # uncomment for trydev

    myJob = self.gateway.createJob()
    myJob.setJobName("SimplePythonLambdaJob")
    myJob.addTask(pythonTask)
    jobId = self.gateway.submitJob(myJob)

    self.assertIsNotNone(jobId)
    self.assertTrue(isinstance(jobId, numbers.Number))
    self.gateway.disconnect()

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

  def test_submit_python_script_from_file(self):
    self.gateway.connect(self.username, self.password)

    script_python = os.getcwd() + '/scripts/random_number.py'

    pythonTask = self.gateway.createPythonTask()
    pythonTask.setTaskName("SimplePythonTaskFromFile")
    pythonTask.setTaskImplementationFromFile(script_python, ['param1', 'param2'])

    myJob = self.gateway.createJob()
    myJob.setJobName("SimplePythonJobFromFile")
    myJob.addTask(pythonTask)
    jobId = self.gateway.submitJob(myJob)

    self.assertIsNotNone(jobId)
    self.assertTrue(isinstance(jobId, numbers.Number))
    
    
    job_result = self.gateway.getJobResult(jobId)

    self.assertIsNotNone(jobId)
    self.assertTrue(RepresentsInt(job_result))
    self.gateway.disconnect()
    
    
    
    self.gateway.disconnect()

  def test_get_job_info(self):
    self.gateway.connect(self.username, self.password)
    jobId = self.gateway.submitWorkflowFromCatalog("basic-examples", "print_file_name")
    job_info = self.gateway.getJobInfo(jobId)
    self.assertTrue(str(job_info.getJobId().value()) == str(jobId))
    self.assertTrue(str(job_info.getJobOwner()) == self.username)
    self.gateway.disconnect()

  def test_get_all_jobs(self):
    self.gateway.connect(self.username, self.password)
    jobId = self.gateway.submitWorkflowFromCatalog("basic-examples", "print_file_name")
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

    script_python = os.getcwd() + '/scripts/random_number.py'
    script_forkenv = os.getcwd() + '/scripts/fork_env.py'

    pythonTask = self.gateway.createPythonTask()
    pythonTask.setTaskName("PythonTaskFromFileWithForkEnv")
    pythonTask.setTaskImplementationFromFile(script_python)

    fork_env = self.gateway.createDefaultForkEnvironment()
    fork_env.setImplementationFromFile(script_forkenv)
    pythonTask.setForkEnvironment(fork_env)

    myJob = self.gateway.createJob()
    myJob.setJobName("SimplePythonJobFromFile")
    myJob.addTask(pythonTask)
    jobId = self.gateway.submitJob(myJob)

    self.assertIsNotNone(jobId)
    self.assertTrue(isinstance(jobId, numbers.Number))
    self.gateway.disconnect()

  def test_submit_python_script_from_file_with_selection_script(self):
    self.gateway.connect(self.username, self.password)
    
    script_python = os.getcwd() + '/scripts/random_number.py'
    
    pythonTask = self.gateway.createPythonTask()
    pythonTask.setTaskName("PythonTaskFromFileWithSelection")
    pythonTask.setTaskImplementationFromFile(script_python)

    selection_script = self.gateway.createDefaultSelectionScript()
    selection_script.setImplementation("selected = True")
    pythonTask.setSelectionScript(selection_script)
    
    myJob = self.gateway.createJob()
    myJob.setJobName("SimplePythonJobFromFile")
    myJob.addTask(pythonTask)
    jobId = self.gateway.submitJob(myJob)
    
    self.assertIsNotNone(jobId)
    self.assertTrue(isinstance(jobId, numbers.Number))
    self.gateway.disconnect()

  def test_submit_with_selection_script_groovy(self):
    self.gateway.connect(self.username, self.password)
    
    script_python = os.getcwd() + '/scripts/random_number.py'
    
    pythonTask = self.gateway.createPythonTask()
    pythonTask.setTaskName("PythonTaskFromFileWithSelectionGroovy")
    pythonTask.setTaskImplementationFromFile(script_python)
        
    selection_script = self.gateway.createSelectionScript(self.gateway.getProactiveScriptLanguage().groovy())
    selection_script.setImplementation("selected = true;")
    pythonTask.setSelectionScript(selection_script)
    
    myJob = self.gateway.createJob()
    myJob.setJobName("SimplePythonJobFromFileGroovySelection")
    myJob.addTask(pythonTask)
    jobId = self.gateway.submitJob(myJob)
    
    self.assertIsNotNone(jobId)
    self.assertTrue(isinstance(jobId, numbers.Number))
    self.gateway.disconnect()


  def test_submit_python_script(self):
    self.gateway.connect(self.username, self.password)

    pythonTask = self.gateway.createPythonTask()
    pythonTask.setTaskName("SimplePythonTask")
    pythonTask.setTaskImplementation("""result = "This is Sparta!"  """)

    myJob = self.gateway.createJob()
    myJob.setJobName("SimplePythonJob")
    myJob.addTask(pythonTask)
    jobId = self.gateway.submitJob(myJob)
    
    job_result = self.gateway.getJobResult(jobId)
    task_result = self.gateway.getTaskResult(jobId,"SimplePythonTask")

    self.assertIsNotNone(jobId)
    self.assertTrue(job_result == 'This is Sparta!' )
    self.assertTrue(job_result == task_result )
    self.gateway.disconnect()

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
  unittest.main()

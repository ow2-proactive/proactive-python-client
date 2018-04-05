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
    jobId = self.gateway.submitPythonLambda(lambda: 88 - 20 * 10, "/usr/bin/python3") # for trydev
    #jobId = self.gateway.submitPythonLambda(lambda: 88 - 20 * 10) # for local server
    self.assertIsNotNone(jobId)
    self.assertTrue(isinstance(jobId, numbers.Number))
    self.gateway.disconnect()

  def test_submit_python_script(self):
    self.gateway.connect(self.username, self.password)
    script_python = '''print('Hello world!')'''
    script_params = {}
    jobId = self.gateway.submitPythonTask(script_python, script_params)
    self.assertIsNotNone(jobId)
    self.assertTrue(isinstance(jobId, numbers.Number))
    self.gateway.disconnect()

  def test_submit_python_script_from_file(self):
    self.gateway.connect(self.username, self.password)
    script_python = os.getcwd() + '/tests/random_number.py'
    script_params = {}
    jobId = self.gateway.submitPythonTaskFromFile(script_python, script_params)
    self.assertIsNotNone(jobId)
    self.assertTrue(isinstance(jobId, numbers.Number))
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


if __name__ == '__main__':
  unittest.main()

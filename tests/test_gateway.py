# -*- coding: utf-8 -*-
import proactive 

import requests
import unittest
import numbers
import os
from unittest.case import skip
import pytest


class GatewayTestSuite(unittest.TestCase):
    """Advanced test cases."""

    
    gateway = None
    username = ""
    password = ""

    @pytest.fixture(autouse=True)
    def setup_gateway(self, metadata):
        self.gateway = proactive.scheduler_gateway(metadata['proactive_url'])
        self.username = metadata['username']
        self.password = metadata['password']
       
    
    
    def test_submit_from_catalog(self):
         self.gateway.connect(self.username, self.password)
         jobId = self.gateway.submitFromCatalog("basic-examples","print_file_name")
         self.assertIsNotNone(jobId)
         self.assertTrue(isinstance(jobId, numbers.Number))
         self.gateway.disconnect()
         
    def test_submit_from_catalog_with_variables(self):
         self.gateway.connect(self.username, self.password)
         jobId = self.gateway.submitFromCatalog("basic-examples","print_file_name", {'file':'test_submit_from_catalog_with_variables'})
         self.assertIsNotNone(jobId)
         self.assertTrue(isinstance(jobId, numbers.Number))     
         self.gateway.disconnect()
    
    def test_submit_file(self):
         self.gateway.connect(self.username, self.password)
         workflow_file_path = os.getcwd() + '/tests/print_file_name.xml'
         jobId = self.gateway.submitFile(workflow_file_path)
         self.assertIsNotNone(jobId)
         self.assertTrue(isinstance(jobId, numbers.Number))    
         self.gateway.disconnect() 
    
         
    def test_submit_file_with_variables(self):
         self.gateway.connect(self.username, self.password)
         workflow_file_path = os.getcwd() + '/tests/print_file_name.xml'
         jobId = self.gateway.submitFile(workflow_file_path, {'file':'test_submit_file_with_variables'})
         self.assertIsNotNone(jobId)
         self.assertTrue(isinstance(jobId, numbers.Number))     
         self.gateway.disconnect()
         
    def test_submit_file(self):
         self.gateway.connect(self.username, self.password)
         workflow_file_path = os.getcwd() + '/tests/print_file_name.xml'
         jobId = self.gateway.submitFile(workflow_file_path)
         self.assertIsNotNone(jobId)
         self.assertTrue(isinstance(jobId, numbers.Number))    
         self.gateway.disconnect() 
    
         
    def test_submit_URL(self):
         self.gateway.connect(self.username, self.password)
         workflow_url = 'https://gist.githubusercontent.com/marcocast/5b9df0478f9e093663eaae36ca2f55b0/raw/ad98492428243db5ebb812205488281b65189077/print_file_name.xml'
         jobId = self.gateway.submitURL(workflow_url, {'file':'test_submit_URL'})
         self.assertIsNotNone(jobId)
         self.assertTrue(isinstance(jobId, numbers.Number))     
         self.gateway.disconnect()
         
    def test_get_job_info(self):
         self.gateway.connect(self.username, self.password)
         jobId = self.gateway.submitFromCatalog("basic-examples","print_file_name")
         job_info = self.gateway.getJobInfo(jobId)
         self.assertTrue(str(job_info.getJobId().value()) == str(jobId))
         self.assertTrue(str(job_info.getJobOwner()) == self.username)
         self.gateway.disconnect()
        

if __name__ == '__main__':
    unittest.main()

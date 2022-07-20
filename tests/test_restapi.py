import proactive
import unittest
import numbers
import os
import pytest


class RestApiTestSuite(unittest.TestCase):
    """Advanced test cases."""

    gateway = None
    username = ""
    password = ""

    @pytest.fixture(autouse=True)
    def setup_gateway(self, metadata):
        self.gateway = proactive.ProActiveGateway(metadata['proactive_url'], debug=True)
        self.username = metadata['username']
        self.password = metadata['password']

    def test_rm_model_hosts(self):
        self.gateway.connect(self.username, self.password)
        restapi = self.gateway.getProactiveRestApi()
        hosts = restapi.get_rm_model_hosts()
        self.assertIsNotNone(hosts)
        self.assertTrue(isinstance(hosts, list))
        self.gateway.disconnect()

    def test_rm_model_nodesources(self):
        self.gateway.connect(self.username, self.password)
        restapi = self.gateway.getProactiveRestApi()
        nodesources = restapi.get_rm_model_nodesources()
        self.assertIsNotNone(nodesources)
        self.assertTrue(isinstance(nodesources, list))
        self.gateway.disconnect()

    def test_rm_model_tokens(self):
        self.gateway.connect(self.username, self.password)
        restapi = self.gateway.getProactiveRestApi()
        tokens = restapi.get_rm_model_tokens()
        self.assertIsNotNone(tokens)
        self.assertTrue(isinstance(tokens, list))
        self.gateway.disconnect()


if __name__ == '__main__':
    unittest.main()

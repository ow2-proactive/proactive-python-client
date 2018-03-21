# -*- coding: utf-8 -*-
import proactive 

import requests
import unittest


class GatewayTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_gateway(self):
         gateway = proactive.scheduler_gateway("http://trydev.activeeon.com:8080","bobot", "proactive")
         print(gateway.submitFromCatalog("basic-examples","native_task_linux"))
        

if __name__ == '__main__':
    unittest.main()

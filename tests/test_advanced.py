# -*- coding: utf-8 -*-
import proactive 

import requests
import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        
        my_client = proactive.scheduler_client("https://trydev.activeeon.com")
        
        sessionid = my_client.pa_connect("", "")
        
        self.assertIsNotNone(sessionid)
       


if __name__ == '__main__':
    unittest.main()

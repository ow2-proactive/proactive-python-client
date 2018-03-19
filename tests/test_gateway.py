# -*- coding: utf-8 -*-
import proactive 

import requests
import unittest


class GatewayTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_gateway(self):
        
        import os
        f = open(os.devnull,"r")
        
        gateway = proactive.scheduler_gateway
        
        print(gateway.getStatus())
        
        
        print(f.read())
             
        

       


if __name__ == '__main__':
    unittest.main()

#! /usr/bin/env python
'''
Try to run all the test cases in the project manually
Seems it can also be done by "python -m unittest discover" from command line
'''


import os
import unittest
import imp

def run_test_cases(verbosity):
    modules = os.listdir('.')
    suite = unittest.TestSuite()
    for module in modules: 
        if module.endswith('.py'):
            testModule = imp.load_source(module[:-3], module)
            suite.addTest(unittest.TestLoader().loadTestsFromModule(testModule))
            
    unittest.TextTestRunner(verbosity=verbosity).run(suite)

def run_all_tests():
    if '-v' in sys.argv:
        verbosity = 2
    else:
        verbosity = 1
    run_test_cases(verbosity)
        
if __name__ == '__main__':
    import sys
    run_all_tests()


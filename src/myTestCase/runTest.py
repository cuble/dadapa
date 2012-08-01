#! /usr/bin/env python

#   Copyright 2012 Chen Gang(fouryusteel@gmail.com)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

'''
Try to run all the test cases in the project manually
Seems it can also be done by "python -m unittest discover" from command line
'''


import os
import unittest

def run_test_cases(verbosity):
    modules = os.listdir('.')
    suite = unittest.TestSuite()
    for module in modules: 
        if module.endswith('.py'):
            testModule = __import__(module[:-3])
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


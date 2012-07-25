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

import os
import sys
import unittest

from stubMockPlugin import mockPlugin
from stubMockPlugin import UnexpectedCallError

def myfun(param):
    return 123
        
class mockPluginTest(unittest.TestCase):
    def setUp(self):
        self.mock = mockPlugin()
        self.mock.setUp()
        
    def test_mock_is_a_singerton(self):
        mock=mockPlugin()
        self.assertEqual(mock, self.mock)
        
    def test_success_if_no_operation(self):
        self.assertRaises(None, self.mock.tearDown())
    
    def test_sucess_mock_function(self):
        self.mock.mock_function(myfun, '123', 10)
        self.assertEqual('myfun', myfun.__name__)
        self.assertEqual(10, myfun('123'))
        self.mock.tearDown()
        self.assertEqual(123, myfun(1))
        
    def test_success_mock_sys_function(self):
        self.mock.mock_function(sys.callstats, '123', 10)
        self.assertEqual('callstats', sys.callstats.__name__)
        self.assertEqual(10, sys.callstats('123'))
        self.mock.tearDown()
        self.assertEqual(None, sys.callstats())

    def test_success_mock_os_function(self):
        orgfun = os.listdir
        self.mock.mock_function(os.listdir, '123', 10)
        self.assertEqual('listdir', os.listdir.__name__)
        self.assertEqual(10, os.listdir('123'))
        self.mock.tearDown()
        self.assertEqual(orgfun, os.listdir)

    def test_fail_if_not_call_mocked_buitin_function(self):
        self.mock.mock_function(sorted, '123',100)
        self.assertEqual('sorted', sorted.__name__)
        with self.assertRaises(UnexpectedCallError) as cm:
            self.mock.tearDown()
        self.assertEqual('\nhaha', str(cm.exception))
        self.assertEqual(['1','2','3'], sorted('132'))

    def test_success_if_mocked_buitin_function_called(self):
        self.mock.mock_function(sorted,'123',10)
        self.assertEqual('sorted', sorted.__name__)
        self.assertEqual(10, sorted('123'))
        self.mock.tearDown()
        self.assertEqual(['1','2','3'], sorted('132'))

if __name__=='__main__':
    unittest.main()
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

import unittest
import sys

from myTestCase import printPlugin
from myTestCase import myTestCase

import stubMockPlugin

def init_stub(self):
    pass

class myTestCaseTest(unittest.TestCase):
    def setUp(self):
        self.org_init = myTestCase.__init__
        myTestCase.__init__ = init_stub
        self.mytc=myTestCase()
        self.mytc.setUp()
        
    def _check_mytc_data_units(self, mytc):
        self.assert_(isinstance(mytc._pp, printPlugin))
        self.assert_(isinstance(mytc._ps, stubMockPlugin.stubPlugin))
        self.assert_(mytc._pm == stubMockPlugin.mockPlugin())
        
    def _check_mytc_function_interface_units(self, mytc):
        self.assertEqual(mytc.check_print_result, mytc._pp.check_print_result)
        self.assertEqual(mytc.stub_out, mytc._ps.stub_out)
        self.assertEqual(mytc.mock_function, mytc._pm.mock_function)
        self.assertEqual(mytc.with_param, mytc._pm.with_param)
        self.assertEqual(mytc.and_return, mytc._pm.and_return)

    def test_no_operation_should_success(self):
        self._check_mytc_data_units(self.mytc)
        self._check_mytc_function_interface_units(self.mytc)
        self.assertRaises(None, self.mytc.tearDown())
        myTestCase.__init__ = self.org_init

class printPluginTest(unittest.TestCase):
    def setUp(self):
        printPlugin.runTest = None
        self.plugin = printPlugin()
        self.plugin.setUp()
    
    def tearDown(self):
        sys.stdout = self.plugin.org_stdout
        
    def test_no_operation_should_success(self):
        self.plugin.tearDown()

    def test_fail_if_print_output_not_checked(self):
        testString = 'Printed should be redirected for later checking'
        print testString
        with self.assertRaises(AssertionError) as cm:
            self.plugin.tearDown()
        self.assertEqual('{0} != {1}\n'.format('',testString), cm.exception.message)

    def test_success_if_print_output_checked(self):
        testStr = 'Printed should be redirected for later checking' 
        print testStr
        self.plugin.check_print_result(testStr+'\n')
        self.plugin.check_print_result('')      
        self.plugin.tearDown()    

    def test_fail_if_print_result_wrong(self):
        print '123'
        self.assertRaises(AssertionError, self.plugin.check_print_result, '456')
        
    def test_success_when_print_and_check_several_times(self):
        print '123'
        self.plugin.check_print_result('123\n')
        print '456'
        self.plugin.check_print_result('456\n')
        print 'kkkazd'
        print '1324'
        self.plugin.check_print_result('kkkazd\n1324\n')
        self.plugin.tearDown()
        
    def test_check_print_result_after_teardown_is_not_allowed(self):
        self.plugin.tearDown()
        self.assertRaises(AttributeError, self.plugin.check_print_result, '')
        
    def test_stdout_should_recover_even_teardown_failed(self):
        print '123'
        self.assertRaises(AssertionError, self.plugin.tearDown) 
        self.assertEqual(sys.stdout, self.plugin.org_stdout)


if __name__=='__main__':
    unittest.main()

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

import myTestCase

class testPlugin:
    def setUp(self, target):
        self.setUp_called = True
        self.target = target
        
    def tearDown(self):
        self.tearDown_called = True

class myTestCaseTest(myTestCase.myTestCase):
    def setUp(self):
        #To Shadow myTestCase's setUp
        self.assertFalse(hasattr(self, 'mySetupCalled'))
        self.assertFalse(hasattr(self, 'myTeardownCalled'))

    def tearDown(self):
        #To Shadow myTestCase's tearDown
        self.assertTrue(self.mySetupCalled)
        self.assertTrue(self.myTeardownCalled)
    
    def my_setup(self):
        self.mySetupCalled = True
        
    def my_teardown(self):
        self.myTeardownCalled = True
    
    def _install_testPlugin_into_plugin_list(self):
        self.tp = testPlugin()
        self.assertFalse(hasattr(self.tp, 'setUp_called'))
        self.assertFalse(hasattr(self.tp, 'tearDown_called'))

        self.org_list = myTestCase._PLUGINLIST
        myTestCase._PLUGINLIST = [self.tp]

    def test_functionanity_with_test_plugin(self):
        self._install_testPlugin_into_plugin_list()
        super(myTestCaseTest, self).setUp()
        self.assertTrue(self.tp.setUp_called) 
        self.assertEqual(self.tp.target, self)       
        super(myTestCaseTest, self).tearDown()
        self.assertTrue(self.tp.tearDown_called)
        myTestCase._PLUGINLIST = self.org_list

    def _check_plugin_install_result(self):
        self.assert_(hasattr(self, 'check_print_result'))
        self.assert_(hasattr(self, 'stub_out'))
        self.assert_(hasattr(self, 'mock_function'))
        self.assert_(hasattr(self, 'with_param'))
        self.assert_(hasattr(self, 'and_return'))

    def test_real_function_result(self):
        self.assertTrue(hasattr(super(myTestCaseTest, self), 'my_setup'))
        self.assertTrue(hasattr(super(myTestCaseTest, self), 'my_teardown'))
        super(myTestCaseTest, self).setUp()
        self._check_plugin_install_result()
        super(myTestCaseTest, self).tearDown()


class myclass:
    pass

class printPluginTest(unittest.TestCase):
    def setUp(self):
        printPlugin.runTest = None
        self.plugin = printPlugin()
        self.target = myclass()
        self.plugin.setUp(self.target)
        
    
    def tearDown(self):
        self.assert_(sys.stdout == self.plugin.org_stdout)
        
    def test_no_operation_should_success(self):
        self.assertEqual(self.plugin.check_print_result, self.target.check_print_result)
        self.assertRaises(None, self.plugin.tearDown())

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
        with self.assertRaises(AssertionError):
            self.plugin.check_print_result('456')
        with self.assertRaises(AssertionError):
            self.plugin.tearDown()
        
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
        with self.assertRaises(AssertionError):
            self.plugin.tearDown()

if __name__=='__main__':
    unittest.main()

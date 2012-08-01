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
from cStringIO import StringIO
#import stubMockPlugin



class myTestCase(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    
def assert_equal(expected, real):
    assert expected==real, '{0} != {1}'.format(expected, real)

class printPlugin:
    def setUp(self):
        self.org_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        try:
            assert_equal('', sys.stdout.getvalue())
        finally:
            sys.stdout = self.org_stdout
                
    def check_print_result(self, expectedString):
        assert_equal(expectedString, sys.stdout.getvalue())
        sys.stdout = StringIO()


#-----------Test Case Part-------------------
class testSut:
    pass

class myTestCaseTest(unittest.TestCase):
    def setUp(self):
        myTestCase.runTest = None  #To make unittest.TestCase.__init__ pass
        self.myTestCase = myTestCase()
        self.myTestCase.setUp()
        self.sut = testSut()

    def test_init_should_success(self):
        self.myTestCase.tearDown()
#mock(wx.App, False, generalMock)
#mockClass(mainWindow)
#generalMock.MainLoop()

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

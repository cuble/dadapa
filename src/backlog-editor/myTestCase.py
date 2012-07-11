#! /usr/bin/env python

import unittest
import mox
import sys
from cStringIO import StringIO

class myTestCase(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    
class printPlugin(unittest.TestCase):
    def setUp(self):
        self.org_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        try:
            self.assertEqual('', sys.stdout.getvalue())
        finally:
            sys.stdout = self.org_stdout
                
    def check_print_result(self, expectedString):
        self.assertEqual(expectedString, sys.stdout.getvalue())
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


class printPluginTest(unittest.TestCase):
    def setUp(self):
        printPlugin.runTest = None
        self.plugin = printPlugin()
        self.plugin.setUp()
    
    def tearDown(self):
        sys.stdout = self.plugin.org_stdout
        
    def test_not_operation_should_success(self):
        self.plugin.tearDown()

    def test_fail_if_print_output_not_checked(self):
        print 'Printed should be redirected for later checking'
        self.assertRaises(AssertionError, self.plugin.tearDown)

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
        
    def test_stdout_should_recover_stdout_even_teardown_failed(self):
        print '123'
        self.assertRaises(AssertionError, self.plugin.tearDown) 
        self.assertEqual(sys.stdout, self.plugin.org_stdout)
#mock(wx.App, False, generalMock)
#mockClass(mainWindow)
#generalMock.MainLoop()

if __name__=='__main__':
    unittest.main()
#! /usr/bin/env python

import sys
import unittest
import os

from myTestCase import assert_equal

class UnexpectedCallError:
    def __reper__(self):
        print "haha"


def mock_func(*param):
    mockPlugin.isMocked = False
    assert_equal(1, len(param))
    assert_equal('123', param[0]) 
    setattr(mocked_module, mocked_func, org_func)
    return 10

class mockInfo:
    def __init__(self, org, new, param, expectRet):
        self.org = org
        self.new = new
        self.param = param
        self.expectRet = expectRet

org_func = ''
mocked_func = ''
mocked_module = ''
def get_module_name(func):
    module_name=func.__module__
    if module_name == 'posix' and 'posix' not in globals() and 'os' in globals():
        module_name = 'os'
    return module_name

class mockPlugin:
    isMocked = False
    def setUp(self):
        mockPlugin.isMocked = False

    def tearDown(self):
        if mockPlugin.isMocked: 
            mockPlugin.isMocked = False
            setattr(mocked_module, mocked_func, org_func)
            raise UnexpectedCallError()
    
    def mock_function(self, func, param, expectedReturn):
        global mocked_func, mocked_module, org_func
        mocked_func = func.__name__
        module_name = get_module_name(func)
        mocked_module = sys.modules[module_name]
        #print mocked_module, mocked_func
        org_func = getattr(mocked_module, func.__name__)
        setattr(mocked_module, func.__name__, mock_func)
        mockPlugin.isMocked = True

def stubfun():
    return 456

class stubPlugin:
    def __init__(self):
        self.orgfun = None
        self.orgModule = None

    def stubOut(self, orgfunc, stubfunc):
        self.orgfun = orgfunc
        self.orgModule = get_module_name(orgfunc)
        module = sys.modules[self.orgModule]
        setattr(module, orgfunc.__name__, stubfunc)
        
    def teardown(self):
        module = sys.modules[self.orgModule]
        setattr(module, self.orgfun.__name__, self.orgfun)

#------------------Test Part--------------
def myfun(param):
    return 123
        
class mockPluginTest(unittest.TestCase):
    def setUp(self):
        self.mock = mockPlugin()
        self.mock.setUp()
        
    def test_success_if_no_operation(self):
        self.mock.tearDown()
    
    def test_sucess_mock_function(self):
        self.mock.mock_function(myfun, '123', 10)
        self.assertEqual(10, myfun('123'))
        self.mock.tearDown()
        self.assertEqual('myfun', myfun.__name__)
        
    def test_success_mock_sys_function(self):
        self.mock.mock_function(sys.callstats, '123', 10)
        self.assertEqual(10, sys.callstats('123'))
        self.mock.tearDown()
        self.assertEqual("callstats", sys.callstats.__name__)

    def test_success_mock_os_function(self):
        self.mock.mock_function(os.listdir, '123', 10)
        self.assertEqual(10, os.listdir('123'))
        self.mock.tearDown()
        self.assertEqual('listdir', os.listdir.__name__)

    def test_fail_if_not_call_mocked_buitin_function(self):
        self.mock.mock_function(sorted, '123',100)
        self.assertRaises(UnexpectedCallError, self.mock.tearDown)
        self.assertEqual(['1','2','3'], sorted('132'))

    def test_success_if_mocked_buitin_function_called(self):
        self.mock.mock_function(sorted,'123',10)
        self.assertEqual(10, sorted('123'))
        self.mock.tearDown()
        self.assertEqual(['1','2','3'], sorted('132'))
        
class stubPluginTest(unittest.TestCase):
    def setUp(self):
        self.stub = stubPlugin()        
    
    def test_stub_myfun_success(self):
        self.stub.stubOut(myfun, stubfun)
        self.assertEqual(456, myfun())
        self.stub.teardown()
        self.assertEqual(123, myfun(1))
                
    def test_stub_sys_func_success(self):
        self.stub.stubOut(sys.callstats, stubfun)
        self.assertEqual(456, sys.callstats())
        self.stub.teardown()
        self.assertEqual("callstats", sys.callstats.__name__)
        
    def test_stub_os_func_success(self):
        self.stub.stubOut(os.listdir, stubfun)
        self.assertEqual(456, os.listdir())
        self.stub.teardown()
        self.assertEqual('listdir', os.listdir.__name__)

if __name__=='__main__':
    unittest.main()

#! /usr/bin/env python

import sys
import os
import types

import unittest
import exceptions
import wx

from myTestCase import assert_equal

def get_module_name(func):
    module_name=func.__module__
    module_dict = globals()
    if module_name in ('posix', 'nt') and module_name not in module_dict and 'os' in module_dict:
        module_name = 'os'
    return module_name

class stubPlugin:
    class stub_imp:
        def __init__(self, do_stub, do_recover):
            self.do_stub = do_stub
            self.do_recover = do_recover
            
    def __init__(self):
        self.orgfuncList = []
        self.stubImpDict = {}
        self.stubImpDict[types.UnboundMethodType] = stubPlugin.stub_imp(self._stub_out_instancemethod, self._recover_instancemethod)
        self.stubImpDict[types.FunctionType] = stubPlugin.stub_imp(self._stub_out_general_function, self._recover_general_function)
        self.stubImpDict[types.BuiltinFunctionType] = stubPlugin.stub_imp(self._stub_out_general_function, self._recover_general_function)
        
    def _stub_out_instancemethod(self, orgfunc, stubfunc):
        setattr(orgfunc.im_class, orgfunc.__name__, stubfunc)
        
    def _recover_instancemethod(self, orgfunc):
        setattr(orgfunc.im_class, orgfunc.__name__, orgfunc)
        
    def _stub_out_general_function(self, orgfunc, stubfunc):
        orgModule = get_module_name(orgfunc)
        sys.modules[orgModule].__dict__[orgfunc.__name__] = stubfunc
        
    def _recover_general_function(self, orgfunc):
        orgModule = get_module_name(orgfunc)
        sys.modules[orgModule].__dict__[orgfunc.__name__] = orgfunc
        
    def stub_out(self, orgfunc, stubfunc):
        self.orgfuncList.append(orgfunc)
        funcType = type(orgfunc)
        if funcType in self.stubImpDict:
            self.stubImpDict[funcType].do_stub(orgfunc, stubfunc)
        else:
            raise TypeError("can't stub function type: {0}".format(str(funcType)))
        
    def teardown(self):
        for orgfunc in self.orgfuncList:
            self.stubImpDict[type(orgfunc)].do_recover(orgfunc)


class UnexpectedCallError:
    def __repr__(self):
        return "\nhaha"

_mockPlugin = None
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

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class mockPlugin(stubPlugin):
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
#        print mocked_module, mocked_func
        org_func = getattr(mocked_module, func.__name__)
        setattr(mocked_module, func.__name__, mock_func)
        mockPlugin.isMocked = True


#------------------Test Part--------------
def myfun(param):
    return 123

class myclass:
    def fun(self, param):
        return param
        
def stubfun():
    return 456

def stubfun_with_one_param(p1):
    return 456

def stub_init_fun(self):
    '''stub init fun, return None'''
    self.param = 456

class stubPluginTest(unittest.TestCase):
    def setUp(self):
        self.stub = stubPlugin()        
    
    def _stub_a_func_success_test(self, target):
        self.stub.stub_out(target, stubfun)
        module=get_module_name(target)
        self.assertEqual(456, sys.modules[module].__dict__[target.__name__]())
        self.stub.teardown()
        self.assertEqual(target.__name__, sys.modules[module].__dict__[target.__name__].__name__)
        
    def test_stub_myfun(self):
        self._stub_a_func_success_test(myfun)
                
    def test_stub_sys_func(self):
        self._stub_a_func_success_test(sys.callstats)
        
    def test_stub_os_func(self):
        self._stub_a_func_success_test(os.listdir)
        
    def test_stub_class_func(self):
        self.stub.stub_out(myclass.fun, stubfun_with_one_param)
        mc=myclass()
        self.assertEqual(456, mc.fun())
        self.stub.teardown()
        self.assertEqual('fun', mc.fun.__name__)
        
    def test_stub_instance_func_is_the_same_as_stub_class_func(self):
        mc=myclass()
        mc1=myclass()
        self.stub.stub_out(mc.fun, stubfun_with_one_param)
        self.assertEqual(456, mc1.fun())
        self.stub.teardown()
        self.assertEqual('fun', mc1.fun.__name__)

    def test_stub_wx_app_func(self):
        self.stub.stub_out(wx.App.__init__, stub_init_fun)
        ma = wx.App()
        self.assertEqual(456, ma.param)
        self.stub.teardown()
        self.assertEqual('__init__', wx.App.__init__.__name__)
        
    def test_stub_unsupported_func_type_failed(self):
        with self.assertRaises(TypeError) as ec:
            self.stub.stub_out(exceptions.Exception.__repr__, stubfun_with_one_param)
        self.assertEqual("can't stub function type: <type 'wrapper_descriptor'>", ec.exception.message)

    def test_stub_three_func(self):
        self.stub.stub_out(myclass.fun, stubfun_with_one_param)
        self.stub.stub_out(myfun, stubfun)
        self.stub.stub_out(wx.App.__init__, stub_init_fun)
        mc = myclass()
        ma = wx.App()
        self.assertEqual(456, myfun())
        self.assertEqual(456, mc.fun())
        self.assertEqual(456, ma.param)
        self.stub.teardown()
        self.assertEqual('myfun', myfun.__name__)
        self.assertEqual('fun', mc.fun.__name__)
        self.assertEqual('__init__', wx.App.__init__.__name__)

        
class mockPluginTest(unittest.TestCase):
    def setUp(self):
        self.mock = mockPlugin()
        self.mock.setUp()
        
    def test_mock_is_a_singerton(self):
        mock=mockPlugin()
        self.assertEqual(mock, self.mock)
        
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
        with self.assertRaises(UnexpectedCallError) as cm:
            self.mock.tearDown()
        self.assertEqual('\nhaha', str(cm.exception))
        self.assertEqual(['1','2','3'], sorted('132'))

    def test_success_if_mocked_buitin_function_called(self):
        self.mock.mock_function(sorted,'123',10)
        self.assertEqual(10, sorted('123'))
        self.mock.tearDown()
        self.assertEqual(['1','2','3'], sorted('132'))

if __name__=='__main__':
    unittest.main()

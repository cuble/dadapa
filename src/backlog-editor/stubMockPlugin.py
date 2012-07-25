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
'''stub and mock plugin to support myTestCase
    * Note: the module can't stub func imported as "from module import func"'''

import sys
import types
import functools

from myTestCase import assert_equal

def get_module_name(func):
    module_name=func.__module__
    if module_name in ('posix', 'nt'):
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
        @functools.wraps(func)
        def mock_func(*param):
            mockPlugin.isMocked = False
            assert_equal(1, len(param))
            assert_equal('123', param[0]) 
            setattr(mocked_module, mocked_func, org_func)
            return 10

        global mocked_func, mocked_module, org_func
        mocked_func = func.__name__
        module_name = get_module_name(func)
        mocked_module = sys.modules[module_name]
#        print mocked_module, mocked_func
        org_func = getattr(mocked_module, func.__name__)
        setattr(mocked_module, func.__name__, mock_func)
        mockPlugin.isMocked = True

if __name__=='__main__':
    print __doc__

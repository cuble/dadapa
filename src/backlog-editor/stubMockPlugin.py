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
        funcType = type(orgfunc)
        if funcType in self.stubImpDict:
            self.stubImpDict[funcType].do_stub(orgfunc, stubfunc)
            self.orgfuncList.append(orgfunc)
        else:
            raise TypeError("can't stub function type: {0}".format(str(funcType)))
        
        
    def teardown(self):
        for orgfunc in self.orgfuncList:
            self.stubImpDict[type(orgfunc)].do_recover(orgfunc)
        self.orgfuncList=[]


def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class mockPlugin:
    class UnexpectedCallError:
        '''The exception raised when user call function not as recorded
        
    It will display the trace information when raised unexpected.
    It may raise:
      when call a mocked function not in the desired sequence
      when teardown but there are still function in wish list 
        '''
        def __init__(self):
            pass
        def __repr__(self):
            return "\n  Expecting Call: sorted('123')\n"

    class mockRecord:
        '''The structured information to be recorded when mock a function
        
    It includes:
      the original function been mocked
      the desired parameter when call the function
      the return value 
        '''
        def __init__(self, orgFunc):
            self.orgFunc = orgFunc
            self.varg = ()
            self.returnVal = None
            
        def set_varg(self, *varg):
            self.varg = varg
            
        def set_return_value(self, val):
            self.returnVal = val
    
    def __init__(self):
        self.stub = stubPlugin()
    
    def setUp(self):
        self._mockRecordList = []

    def tearDown(self):
        self.stub.teardown()
        if self._mockRecordList != []: 
            self._mockRecordList = []
            raise self.UnexpectedCallError()
    
    def mock_function(self, func):
        @functools.wraps(func)
        def mock_func(*varg, **karg):
            firstRecord = self._mockRecordList[0]
            if firstRecord.orgFunc.__name__ != mock_func.__name__:
                raise self.UnexpectedCallError()
            if firstRecord.varg != varg:
                raise self.UnexpectedCallError()
            self._mockRecordList.pop(0)
            return firstRecord.returnVal

        record = self.mockRecord(func)
        self._mockRecordList.append(record)
        self.stub.stub_out(func, mock_func)
        return self
        
    def with_param(self, *varg, **karg):
        self._mockRecordList[-1].set_varg(*varg) 
        return self
    
    def and_return(self, val):
        self._mockRecordList[-1].set_return_value(val) 
        return self

if __name__=='__main__':
    print __doc__

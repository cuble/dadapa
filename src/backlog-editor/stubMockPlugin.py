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
        setattr(orgfunc.im_class, orgfunc.__name__, orgfunc.im_func)
        
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
    class UnexpectedCallError(BaseException):
        '''The exception raised when user call function not as recorded
        
    It will display the trace information when raised unexpected.
    It may raise:
      when call a mocked function not in the desired sequence
      when teardown but there are still function in wish list 
        '''
        def __init__(self, expectedCallInfo, realCallInfo=None):
            self.expect = expectedCallInfo
            self.real = realCallInfo

        def __repr__(self):
            info =      "\n    Expecting Call: " + repr(self.expect)
            if self.real: 
                info += "\n    But Actual Is:  " + repr(self.real)
            info += "\n"
            return info

    class mockRecord:
        '''The structured information to be recorded when mock a function
        
    It includes:
      the original function been mocked
      the desired parameter when call the function
      the return value 
        '''
        def __init__(self, orgFunc, *varg, **karg):
            self.orgFunc = orgFunc
            self.varg = varg
            self.karg = karg
            self.returnVal = None
            
        def set_varg(self, *varg, **karg):
            if self.varg != () or self.karg != {}:
                raise SyntaxError('expected param already set')
            self.varg = varg
            self.karg = karg
            
        def set_return_value(self, val):
            self.returnVal = val
            
        def __ne_two_class_func(self, other):
            if self.orgFunc.im_class != other.orgFunc.im_class: 
                return True
            if self.orgFunc.im_self and other.orgFunc.im_self:
                return self.orgFunc.im_self != other.orgFunc.im_self
            return False
        
        def __ne_class_func_to_general_func(self, other):
            if len(other.varg)==0: return True
            if self.orgFunc.im_self: 
                if self.orgFunc.im_self == other.varg[0]:
                    other.varg = other.varg[1:]
                else: return True
            else:
                if isinstance(other.varg[0], self.orgFunc.im_class):
                    other.varg = other.varg[1:]
                else: return True            
            return False

        def __ne_class_info(self, other):
            if hasattr(self.orgFunc, 'im_class'):
                if hasattr(other.orgFunc, 'im_class'):
                    if self.__ne_two_class_func(other): 
                        return True
                else:
                    if self.__ne_class_func_to_general_func(other):
                        return True
            else:
                if hasattr(other.orgFunc, 'im_class'):
                    if other.__ne_class_func_to_general_func(self):
                        return True
            return False

        def __eq__(self, other):
#            print self.varg, self.karg, other.varg, other.karg
            if self.__ne_class_info(other): return False
            if self.orgFunc.__name__ == other.orgFunc.__name__\
              and self.varg == other.varg\
              and self.karg == other.karg:
                return True
            else:
                return False
            
        def __ne__(self, other):
            return not self.__eq__(other)
        
        def __repr__(self):
            callStr = self.orgFunc.__name__
            argStr = ", ".join(repr(v) for v in self.varg)
            if hasattr(self.orgFunc, 'im_class'):
                obj = self.orgFunc.im_class
                if self.orgFunc.im_self: obj = self.orgFunc.im_self
                if argStr == '': argStr = repr(obj)
                else: argStr = repr(obj) + ', ' + argStr
            kargStr = ""
            for k in sorted(self.karg.keys()):
                kargStr = kargStr + ", " + str(k) + "=" +\
                 repr(self.karg[k]) 
            callStr += "(" + argStr + kargStr + ")"
            return callStr 

    
    def __init__(self):
        self.stub = stubPlugin()
    
    def setUp(self):
        self._mockRecordList = []

    def tearDown(self):
        self.stub.teardown()
        if self._mockRecordList != []: 
            firstRecord = self._mockRecordList[0]
            self._mockRecordList = []
            raise mockPlugin().UnexpectedCallError(firstRecord)
        
    def mock_function(self, func):
        @functools.wraps(func)
        def mock_func(*varg, **karg):
            firstRecord = self._mockRecordList[0]
            realCall = mockPlugin().mockRecord(mock_func, *varg, **karg)
            if firstRecord != realCall:
                raise mockPlugin().UnexpectedCallError(firstRecord, realCall)
#            if firstRecord.orgFunc.__name__ != mock_func.__name__:
#                realCall = mockPlugin().mockRecord(mock_func, *varg, **karg)
#                raise mockPlugin().UnexpectedCallError(firstRecord, realCall)
#            if hasattr(firstRecord.orgFunc, 'im_class'):
#                if not isinstance(varg[0], firstRecord.orgFunc.im_class) :
#                    realCall = mockPlugin().mockRecord(mock_func, *varg, **karg)
#                    raise mockPlugin().UnexpectedCallError(firstRecord, realCall)
#            else:
#                if firstRecord.varg != varg or firstRecord.karg != karg:
##                    print varg, firstRecord.varg
#                    realCall = mockPlugin().mockRecord(mock_func, *varg, **karg)
#                    raise mockPlugin().UnexpectedCallError(firstRecord, realCall)
            self._mockRecordList.pop(0)
            return firstRecord.returnVal

        record = mockPlugin().mockRecord(func)
        self._mockRecordList.append(record)
        self.stub.stub_out(func, mock_func)
        return self
        
    def with_param(self, *varg, **karg):
        self._mockRecordList[-1].set_varg(*varg, **karg) 
        return self
    
    def and_return(self, val):
        self._mockRecordList[-1].set_return_value(val) 
        return self

if __name__=='__main__':
    print __doc__

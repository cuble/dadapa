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

import sys
import os
import unittest

from stubMockPlugin import stubPlugin
from stubMockPlugin import get_module_name

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
    '''stub init fun, return None is needed'''
    self.param = 456

_wxNotImported = True
try:
    import wx
    _wxNotImported = False
except ImportError:
    print "Warning: wxPython not installed, some test cases related will not included"

def ignoreIfwxPythonNotInstalled():
    return unittest.skipIf(_wxNotImported, 'import wx failed, execute the case will cause exception')

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

    @ignoreIfwxPythonNotInstalled()
    def test_stub_wx_app_func(self):
        self.stub.stub_out(wx.App.__init__, stub_init_fun)
        ma = wx.App()
        self.assertEqual(456, ma.param)
        self.stub.teardown()
        self.assertEqual('__init__', wx.App.__init__.__name__)
        
    def test_stub_unsupported_func_type_failed(self):
        with self.assertRaises(TypeError) as ec:
            self.stub.stub_out(sorted.__repr__, stubfun_with_one_param)
        self.assertEqual("can't stub function type: <type 'method-wrapper'>", ec.exception.message)

    @ignoreIfwxPythonNotInstalled()
    def test_stub_three_func(self):
        self.stub.stub_out(myclass.fun, stubfun_with_one_param)
        self.stub.stub_out(myfun, stubfun)
        self.stub.stub_out(os.listdir, stubfun)
        self.stub.stub_out(wx.App.__init__, stub_init_fun)
        mc = myclass()
        ma = wx.App()
        self.assertEqual(456, myfun())
        self.assertEqual(456, mc.fun())
        self.assertEqual(456, ma.param)
        self.assertEqual(456, os.listdir())
        self.stub.teardown()
        self.assertEqual('myfun', myfun.__name__)
        self.assertEqual('fun', mc.fun.__name__)
        self.assertEqual('__init__', wx.App.__init__.__name__)
        self.assertEqual('listdir', os.listdir.__name__)
        
if __name__=='__main__':
    unittest.main()


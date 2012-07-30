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

import os
import sys
import unittest

from stubMockPlugin import mockPlugin

def myfun():
    return 123

class myClass:
    def fun(self):
        return 'real fun in myClass'

    
class mockPluginTest(unittest.TestCase):
    def setUp(self):
        self.mock = mockPlugin()
        self.mock.setUp()
        
    def tearDown(self):
        try:
            self.mock.tearDown()
        except mockPlugin().UnexpectedCallError:
            #accessed private member just for test
            self.assertEqual([],self.mock._mockRecordList)

        
    def test_mock_is_a_singerton(self):
        mock=mockPlugin()
        self.assertEqual(mock, self.mock)
        
    def test_success_if_no_operation(self):
        self.assertRaises(None, self.mock.tearDown())
    
    def test_sucess_mock_myfun(self):
        self.mock.mock_function(myfun).with_param('123', '456')
        self.assertEqual(None, myfun('123', '456'))
        self.mock.tearDown()
        self.assertEqual(123, myfun())
        
    def test_success_mock_sys_function(self):
        self.mock.mock_function(sys.callstats).and_return(1)
        self.assertEqual(1, sys.callstats())
        self.mock.tearDown()
        self.assertEqual(None, sys.callstats())

    def test_success_mock_os_function(self):
        orgfun = os.chdir
        self.mock.mock_function(os.chdir).with_param('.').and_return(True)
        self.assertEqual(True, os.chdir('.'))
        self.mock.tearDown()
        self.assertEqual(orgfun, os.chdir)

    def test_success_mock_function_in_myclass(self):
        self.mock.mock_function(myClass.fun).with_param(1).and_return(2)
        c=myClass()
        self.assertEqual(2, c.fun(1))
        self.mock.tearDown()
        self.assertEqual('real fun in myClass', c.fun())

    def test_success_mock_buitin_function(self):
        self.mock.mock_function(sorted).with_param('123').and_return(10)
        self.assertEqual(10, sorted('123'))
        self.mock.tearDown()
        self.assertEqual(['1','2','3'], sorted('132'))

    def test_mock_with_key_param(self):
        self.mock.mock_function(myfun).with_param(1,2,3,p1=4,p2=5)
        self.assertEqual(None, myfun(1,2,3, p1=4, p2=5))
        self.mock.tearDown()
                
    def test_success_mock_several_functions(self):
        self.mock.mock_function(myfun).and_return('myfun')
        self.mock.mock_function(sorted).with_param('AnythingIsOk', p='aKeyParam')
        self.mock.mock_function(os.chdir).with_param('..').and_return('aObject')
        self.assertEqual('myfun', myfun())
        self.assertEqual(None, sorted('AnythingIsOk', p='aKeyParam'))
        self.assertEqual('aObject', os.chdir('..'))
        self.mock.tearDown()
        self.assertEqual(123, myfun())
        self.assertEqual(['1', '2', '3'], sorted('132'))
        self.assertEqual(None, os.chdir('.'))

    def _check_unexpectedCall_exception_content(self, exception, expect, real):
        self.assertEqual(expect, exception.expect)
        self.assertEqual(real, exception.real)

    def test_fail_if_not_call_mocked_function(self):
        self.mock.mock_function(sorted).with_param('123').and_return(10)
        self.assertEqual('sorted', sorted.__name__)
        with self.assertRaises(mockPlugin().UnexpectedCallError) as cm:
            self.mock.tearDown()
        expect = mockPlugin().mockRecord(sorted, '123')
        self._check_unexpectedCall_exception_content(cm.exception, expect, None)
        self.assertEqual(['1','2','3'], sorted('132'))
        
    def test_fail_if_mocked_function_call_in_wrong_sequence(self):
        self.mock.mock_function(myfun).and_return('myfun')
        self.mock.mock_function(sorted).with_param('AnythingIsOk')
        with self.assertRaises(mockPlugin().UnexpectedCallError) as cm:
            sorted()        
        expect = mockPlugin().mockRecord(myfun)
        real = mockPlugin().mockRecord(sorted)
        self._check_unexpectedCall_exception_content(cm.exception, expect, real)

    def test_fail_if_param_not_the_expected(self):
        self.mock.mock_function(myfun).with_param(1,'1','anything')
        with self.assertRaises(mockPlugin().UnexpectedCallError) as cm:
            myfun(1,1)
        expect = mockPlugin().mockRecord(myfun, 1, '1', 'anything')
        real = mockPlugin().mockRecord(myfun, 1, 1)
        self._check_unexpectedCall_exception_content(cm.exception, expect, real)
        
    def test_fail_if_key_param_not_the_same(self):
        self.mock.mock_function(myfun).with_param(1,p1=2,p2=3)
        with self.assertRaises(mockPlugin().UnexpectedCallError) as cm:
            myfun(1,p1=2)
        expect = mockPlugin().mockRecord(myfun, 1, p1=2, p2=3)
        real = mockPlugin().mockRecord(myfun, 1, p1=2)
        self._check_unexpectedCall_exception_content(cm.exception, expect, real)

    def test_fail_if_set_param_after_param_already_set(self):
        with self.assertRaises(SyntaxError) as cm:
            self.mock.mock_function(myfun).with_param(1).with_param(2)
        self.assertEqual('expected param already set', str(cm.exception))

    def test_fail_if_set_param_after_key_param_already_set(self):
        with self.assertRaises(SyntaxError) as cm:
            self.mock.mock_function(myfun).with_param(p=1).with_param(2)
        self.assertEqual('expected param already set', str(cm.exception))

class mockRecordTest(unittest.TestCase):
    def test_two_record_equal(self):
        record_1 = mockPlugin().mockRecord(myfun, 1, p1=1)
        record_2 = mockPlugin().mockRecord(myfun, 1, p1=1)
        self.assertEqual(record_1, record_2)
        
    def test_two_record_not_equal_if_func_name_different(self):
        record_1 = mockPlugin().mockRecord(myfun)
        record_2 = mockPlugin().mockRecord(sorted)
        self.assertNotEqual(record_1, record_2)

    def test_two_record_not_equal_if_param_different(self):
        record_1 = mockPlugin().mockRecord(myfun)
        record_2 = mockPlugin().mockRecord(myfun, 1)
        self.assertNotEqual(record_1, record_2)

    def test_two_record_not_equal_if_key_param_different(self):
        record_1 = mockPlugin().mockRecord(myfun)
        record_2 = mockPlugin().mockRecord(myfun, p1=1)
        self.assertNotEqual(record_1, record_2)
        
    def test_two_record_not_equal_if_both_param_different(self):
        record_1 = mockPlugin().mockRecord(myfun,1)
        record_2 = mockPlugin().mockRecord(myfun, p1=1)
        self.assertNotEqual(record_1, record_2)
        
class unexpectedCallExceptionTest(unittest.TestCase):
    def setUp(self):
        self.c = myClass()
        
    def test_expect_call_not_come(self):
        expect = mockPlugin().mockRecord(myfun,1)
        e = mockPlugin().UnexpectedCallError(expect)
        expectStr = '''
    Expecting Call: myfun(1)
'''
        self.assertEqual(expectStr, str(e))
        
    def test_expect_call_not_come_with_string_param(self):
        expect = mockPlugin().mockRecord(myfun,'1')
        e = mockPlugin().UnexpectedCallError(expect)
        expectStr = '''
    Expecting Call: myfun('1')
'''
        self.assertEqual(expectStr, str(e))
        
    def test_expect_call_not_come_with_class_param(self):
        expect = mockPlugin().mockRecord(myfun, self.c)
        e = mockPlugin().UnexpectedCallError(expect)
        expectStr = '''
    Expecting Call: myfun({0})
'''.format(repr(self.c))
        self.assertEqual(expectStr, str(e))
        
    def test_expect_call_not_come_with_key_param(self):
        expect = mockPlugin().mockRecord(myfun, '123', p1=1, p2='good afternoon', p3=self.c)
        e = mockPlugin().UnexpectedCallError(expect)
        expectStr = '''
    Expecting Call: myfun('123', p1=1, p2='good afternoon', p3={0})
'''.format(repr(self.c))
        self.assertEqual(expectStr, str(e))
        
    def test_invalid_call_(self):
        expect = mockPlugin().mockRecord(myfun, 'happy', p1=600, p2='good afternoon', p3=self.c)
        real = mockPlugin().mockRecord(sorted, 123, p='bad', test=self.c)
        e = mockPlugin().UnexpectedCallError(expect, real)
        expectStr = '''
    Expecting Call: myfun('happy', p1=600, p2='good afternoon', p3={0})
    But Is: sorted(123, p='bad', test={1})
'''.format(repr(self.c),repr(self.c))
        self.assertEqual(expectStr, str(e))

if __name__=='__main__':
    unittest.main()
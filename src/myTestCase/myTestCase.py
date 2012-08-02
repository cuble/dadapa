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
import stubMockPlugin



class myTestCase(unittest.TestCase):
    def setUp(self):
        self._pp = printPlugin()
        self.check_print_result = self._pp.check_print_result
        self._ps = stubMockPlugin.stubPlugin()
        self.stub_out = self._ps.stub_out
        self._pm = stubMockPlugin.mockPlugin()
        self.mock_function = self._pm.mock_function
        self.with_param = self._pm.with_param
        self.and_return = self._pm.and_return
        #
#    def tearDown(self):
#        print 'myTestCase tearDown'
#        self.my_teardown()
    pass

def assert_equal(expected, real):
    assert expected==real, '{0} != {1}'.format(expected, real)

class printPlugin:
    def setUp(self, target):
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



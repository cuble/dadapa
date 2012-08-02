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


def assert_equal(expected, real):
    assert expected==real, '{0} != {1}'.format(expected, real)

class printPlugin:
    def setUp(self, target):
        self.org_stdout = sys.stdout
        sys.stdout = StringIO()
        target.check_print_result = self.check_print_result

    def tearDown(self):
        try:
            assert_equal('', sys.stdout.getvalue())
        finally:
            sys.stdout = self.org_stdout
                
    def check_print_result(self, expectedString):
        assert_equal(expectedString, sys.stdout.getvalue())
        sys.stdout = StringIO()

_PLUGINLIST = [printPlugin(),
               stubMockPlugin.stubPlugin(), 
               stubMockPlugin.mockPlugin()]

class myTestCase(unittest.TestCase):
    def setUp(self):
        for plugin in _PLUGINLIST:
            plugin.setUp(self)
            
        self.my_setup()

    def tearDown(self):
        for plugin in _PLUGINLIST:
            plugin.tearDown()
            
        self.my_teardown()

    def my_setup(self):
        pass
    
    def my_teardown(self):
        pass


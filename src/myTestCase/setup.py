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

from distutils.core import setup

if __name__=='__main__':
    setup(name='myTestCase',
      version='0.1',
      py_modules=['myTestCase', 'stubMockPlugin'],
      url='https://github.com/cuble/dadapa/tree/master/src/myTestCase',
      maintainer='Chen Gang',
      maintainer_email='fouryusteel@gmail.com',
      license='Apache License, Version 2.0',
      description='a UT framework derived from unittest.TestCase',
      long_description='''myTestCase is UT framework derived from unittest.TestCase
It's designed to simplify TDD with Python
Features:
    1. stdout is redirected in myTestCase, print result should be checked
    2. function stubed by myTestCase will be unstub automatically
    3. mock generation function and class function are supported'''
      )

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

import myTestCase as mtc
import backlogTree

class testFile:
    def close(self):
        pass

    def write(self):
        pass

class myInterfaceTest(mtc.myTestCase):
    def test_my_open_is_wrap_to_open(self):
        fileName = 'another file'
        flag = 'w+'
        content = ['contents\n']
        self.mock_function(open).with_param(fileName, flag).and_return(content)
        self.assertEqual(content, backlogTree.my_open(fileName, flag))

    def test_my_open_is_wrap_to_open_with_default_flag_r(self):
        self.mock_function(open).with_param('another file', 'rb').and_return([])
        self.assertEqual([], backlogTree.my_open('another file'))

    def test_my_close_is_wrap_to_file_close(self):
        checkStr = 'for checking only'
        f = testFile()
        self.mock_function(f.close).and_return(checkStr)
        self.assertEqual(checkStr, backlogTree.my_close(f))
        
    def test_my_write_is_wrap_to_file_write(self):
        testStr = 'for checking only'
        f = testFile()
        self.mock_function(f.write).with_param(testStr)
        backlogTree.my_write(f, testStr)

btC=backlogTree.backlogTree
class backlogFileTest:
    testDataList=\
[
('two first level subTree', 
    ['sub content 1\n', 
     'sub content 2\n'],
    [btC('sub content 1'), btC('sub content 2')] ),
('two first level subTree with blank lines',
    [' \n',
     '\t\n',
     'sub content 1\n',
     '\t   \t\n',
     'sub content 2\n'],
    [btC('sub content 1'), btC('sub content 2')] ),
('two first level subTree both with subTree',
    ['first level sub content 1\n',
     '  first level sub content 1: sub item\n',
     'first level sub content 2\n',
     '  first level sub content 2: sub item\n'],
    [btC('first level sub content 1', 
       [btC('first level sub content 1: sub item')] ),
     btC('first level sub content 2', 
       [btC('first level sub content 2: sub item')] )
    ] ),
('More level subTree',
    ['first level sub content 1\n',
     '  second level sub content 1\n',
     '    third level sub content 1\n'],
    [btC('first level sub content 1', 
       [btC('second level sub content 1',
          [btC('third level sub content 1')] )
       ] )
    ] ),
('two level subTree with more indent',
    ['first level sub content 1\n',
     '    first level sub content 1: sub item\n'],
    [btC('first level sub content 1',  
       [btC('first level sub content 1: sub item')] )
    ] ),
('two level subTree while tab equals to 4 spaces',
    ['first level sub content 1\n',
     '\t\tfirst level sub content 1: sub item 1\n',
     '        first level sub content 1: sub item 2\n',
     '    \tfirst level sub content 1: sub item 3\n'],
    [btC('first level sub content 1',
       [btC('first level sub content 1: sub item 1'),
        btC('first level sub content 1: sub item 2'),
        btC('first level sub content 1: sub item 3')] )
    ] ),
('More level subTree with not regular indent',
    ['  sub content 1\n',
     '        sub content 1.1\n',
     '      sub content 1.2\n',
     '       sub content 1.2.1\n',
     '    sub content 1.3',
     'sub content 2\n'],
    [btC('sub content 1',
       [btC('sub content 1.1'),
        btC('sub content 1.2', [btC('sub content 1.2.1')]),
        btC('sub content 1.3')] ),
     btC('sub content 2')
    ] )
]

    testDataWithAttr = \
[
('two first level nodes',
    ['sub content 1\n',
     '{"attribute":"value"}\n',
     'sub content 2\n',
     '{"attribute":"value"}\n'],
    [btC('sub content 1', attribute={'attribute':'value'}),
     btC('sub content 2', attribute={'attribute':'value'})] ),
('two level nodes',
    ['sub content 1\n',
     '{"attribute":"value"}\n',
     '  sub content 1.2\n',
     '  {"attribute":"sub value"}\n'],
    [btC('sub content 1',
         [btC('sub content 1.2', attribute={'attribute':'sub value'})], 
         {'attribute':'value'})] )
]

    def __init__(self, *testData):
        self.name = testData[0]
        self.content = testData[1]
        self.subTree = testData[2]
    
    def _do_mock(self, testCase):
        testCase.mock_function(backlogTree.my_open).with_param(self.name).and_return(self.content)
        testCase.mock_function(backlogTree.my_close).with_param(self.content)
        
    def test_init_from_from_file_base_blank_node(self, testCase):
        self._do_mock(testCase)
        bt = btC()
        bt.init_from_file(self.name)
        testCase.assertEqual(self.name, bt._content)
        testCase.assertEqual(btC.defaultAttr, bt._attribute)
        testCase.assertEqual(self.subTree, bt._subTree)
            
def write_stub(f, content):
    f.append(content)
      
class backlogTreeTest(mtc.myTestCase):
    def my_setup(self):
        pass
    
    def my_teardown(self):
        pass
    
    def _check_backlog_tree_content(self, bt, content, attr, subTree):
        self.assertEqual(bt._content, content)
        self.assertEqual(bt._attribute, attr)
        self.assertEqual(bt._subTree, subTree)

    def test_create_blank_tree(self):
        bt = btC()
        self._check_backlog_tree_content(bt, '', btC.defaultAttr, [])
        
    def test_create_one_node_tree(self):
        content = 'root node'
        attribute = {'priority':2}
        bt = btC(content, [], attribute)
        self._check_backlog_tree_content(bt, content, attribute, [])
                
    def test_init_from_file_base_blank_tree(self):
        for bftData in backlogFileTest.testDataList:
            bft = backlogFileTest(*bftData)
            bft.test_init_from_from_file_base_blank_node(self)

    def test_init_from_file_base_inited_node(self):
        fileName = 'a backlog'
        content = ['sub content 1\n']
        self.mock_function(backlogTree.my_open).with_param(fileName).and_return(content)
        self.mock_function(backlogTree.my_close).with_param(content)
        bt = btC('root node', attribute={'priority': 2})
        bt.init_from_file(fileName)
        self.assertEqual('root node', bt._content)
        self.assertEqual({'priority':2}, bt._attribute)
        self.assertEqual(bt._subTree, [btC('sub content 1', attribute={'priority': 2})])
        
    def test_init_from_file_with_attribute(self):
        for bftData in backlogFileTest.testDataWithAttr:
            bft = backlogFileTest(*bftData)
            bft.test_init_from_from_file_base_blank_node(self)
                
    def test_save_blank_node_to_file(self):
        fileName = 'a project'
        content = []
        bt = btC()
        self.mock_function(backlogTree.my_open).with_param(fileName, 'wb').and_return(content)
        self.mock_function(backlogTree.my_close).with_param(content)
        self.stub_out(backlogTree.my_write, write_stub)
        bt.save(fileName)
        self.assertEqual(content, [])
        
    def test_save_one_node_to_file(self):
        fileName = 'another project'
        content = []
        bt = btC('root node')
        self.mock_function(backlogTree.my_open).with_param(fileName, 'wb').and_return(content)
        self.mock_function(bt.__str__).and_return('backlogTree represent')
        self.mock_function(backlogTree.my_close).with_param(content)
        self.stub_out(backlogTree.my_write, write_stub)
        bt.save(fileName)
        self.assertEqual(['backlogTree represent'], content)

if __name__ == '__main__':
    import unittest
    unittest.main()

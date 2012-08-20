import myTestCase as mtc
import backlogTree

class testFile:
    def close(self):
        pass

class ownInterfaceTest(mtc.myTestCase):
    def test_my_open_is_wrap_to_open(self):
        fileName = 'another file'
        flag = 'w+'
        content = ['contents\n']
        self.mock_function(open).with_param(fileName, flag).and_return(content)
        self.assertEqual(content, backlogTree.my_open(fileName, flag))

    def test_my_open_is_wrap_to_open_with_default_flag_r(self):
        self.mock_function(open).with_param('another file', 'r').and_return([])
        self.assertEqual([], backlogTree.my_open('another file'))

    def test_my_close_is_wrap_to_close(self):
        checkStr = 'for checking only'
        f = testFile()
        self.mock_function(f.close).and_return(checkStr)
        self.assertEqual(checkStr, backlogTree.my_close(f))

class fileTest:
    testDataForBlankTreeInit=\
[
    ('two first level subTree', 
        ['sub content 1\n', 
         'sub content 2\n'],
        [backlogTree.backlogTree('sub content 1'), backlogTree.backlogTree('sub content 2')]
    ),
    ('two first level subTree with blank lines',
        [' \n',
         '\t\n',
         'sub content 1\n',
         '\t   \t\n',
         'sub content 2\n'],
        [backlogTree.backlogTree('sub content 1'), backlogTree.backlogTree('sub content 2')]
    ),
    ('two level subTree',
        ['first level sub content 1\n',
         '\tfirst level sub content 1: sub item\n'],
         [backlogTree.backlogTree('first level sub content 1', backlogTree.backlogTree.defaultAttr, 
            [backlogTree.backlogTree('first level sub content 1: sub item')]
                                 )
         ]
    ),
    ('two first level subTree both with subTree',
        ['first level sub content 1\n',
         '  first level sub content 1: sub item\n',
         'first level sub content 2\n',
         '  first level sub content 2: sub item\n'],
         [backlogTree.backlogTree('first level sub content 1', backlogTree.backlogTree.defaultAttr, 
            [backlogTree.backlogTree('first level sub content 1: sub item')]
                                 ),
          backlogTree.backlogTree('first level sub content 2', backlogTree.backlogTree.defaultAttr, 
            [backlogTree.backlogTree('first level sub content 2: sub item')]
                                 )
         ]
    )
]

    def __init__(self, *testData):
        self.name = testData[0]
        self.content = testData[1]
        self.subTree = testData[2]
    
    def _do_mock(self, testCase):
        testCase.mock_function(backlogTree.my_open).with_param(self.name).and_return(self.content)
        testCase.mock_function(backlogTree.my_close).with_param(self.content)
        
    def test_init_blank_node_from_file(self, testCase):
        defaultAttr = backlogTree.backlogTree.defaultAttr
        self._do_mock(testCase)
        bt = backlogTree.backlogTree()
        bt.init_from_file(self.name)
        testCase.assertEqual(self.name, bt._content)
        testCase.assertEqual(bt._attribute, defaultAttr)
        testCase.assertEqual(bt._subTree, self.subTree)
            
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
        bt = backlogTree.backlogTree()
        self._check_backlog_tree_content(bt, '', backlogTree.backlogTree.defaultAttr, [])
        
    def test_create_one_node_tree(self):
        content = 'root node'
        attribute = {'priority':2}
        bt = backlogTree.backlogTree(content, attribute)
        self._check_backlog_tree_content(bt, content, attribute, [])
                
    def test_init_blank_tree_from_file_other_cases(self):
        testCaseNum = len(fileTest.testDataForBlankTreeInit)
        for i in range(testCaseNum):
            ft = fileTest(*fileTest.testDataForBlankTreeInit[i])
            ft.test_init_blank_node_from_file(self)

    def test_init_one_node_tree_from_file_filename_is_ignored(self):
        fileName = 'a backlog'
        content = ['sub content 1\n', 'sub content 2\n']
        self.mock_function(backlogTree.my_open).with_param(fileName).and_return(content)
        self.mock_function(backlogTree.my_close).with_param(content)
        bt = backlogTree.backlogTree('root node', {'priority':2})
        bt.init_from_file(fileName)
        self.assertEqual('root node', bt._content)
        self.assertEqual({'priority':2}, bt._attribute)
        self.assertEqual(bt._subTree, [backlogTree.backlogTree('sub content 1', {'priority':2}),
                                       backlogTree.backlogTree('sub content 2', {'priority':2})])
        
if __name__ == '__main__':
    import unittest
    unittest.main()

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

class backlogTreeTest(mtc.myTestCase):
    class fileTest:
        def __init__(self, fileName, fileContent, subTree):
            self.name = fileName
            self.content = fileContent
            self.subTree = subTree
            
    file_test_data=[
('two first level subtree', 
['sub content 1\n', 
           'sub content 2\n'],
[backlogTree.backlogTree('sub content 1'), backlogTree.backlogTree('sub content 2')]),
()]
    
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
        
    def test_init_blank_tree_from_file_root_content_is_file_name(self):
        fileName = 'a backlog'
        content = ['sub content 1\n', 'sub content 2\n']
        defaultAttr = backlogTree.backlogTree.defaultAttr
        self.mock_function(backlogTree.my_open).with_param(fileName).and_return(content)
#        self.mock_function(backlogTree.my_close).with_param(content)
        bt = backlogTree.backlogTree()
        bt.init_from_file(fileName)
        self.assertEqual(fileName, bt._content)
        self.assertEqual(bt._attribute, defaultAttr)
        self.assertEqual(bt._subTree, [backlogTree.backlogTree('sub content 1'),
                                       backlogTree.backlogTree('sub content 2')])

    def test_init_one_node_tree_from_file_file_name_is_ignored(self):
        fileName = 'a backlog'
        content = ['sub content 1\n', 'sub content 2\n']
        self.mock_function(backlogTree.my_open).with_param(fileName).and_return(content)
        bt = backlogTree.backlogTree('root node', {'priority':2}, [])
        bt.init_from_file(fileName)
        self.assertEqual('root node', bt._content)
        self.assertEqual({'priority':2}, bt._attribute)
        self.assertEqual(bt._subTree, [backlogTree.backlogTree('sub content 1', {'priority':2}),
                                       backlogTree.backlogTree('sub content 2', {'priority':2})])
        
    def test_init_muti_level_tree_from_file(self):
        fileName = '2 level backlog'
        content = ['sub content 1\n', '  sub content 1: sub 1  \n', '  sub content 1: sub 2\n', 'sub content 2\n']
        defaultAttr = backlogTree.backlogTree.defaultAttr
        self.mock_function(backlogTree.my_open).with_param(fileName).and_return(content)
        bt = backlogTree.backlogTree()
        bt.init_from_file(fileName)
        self.assertEqual(fileName, bt._content)
        self.assertEqual(bt._attribute, defaultAttr)
        sub_bt1_sub1 = backlogTree.backlogTree('sub content 1: sub 1')
        sub_bt1_sub2 = backlogTree.backlogTree('sub content 1: sub 2')
#        self.assertEqual(bt._subTree, [backlogTree.backlogTree('sub content 1', [sub_bt1_sub1, sub_bt1_sub2]),
#                                       backlogTree.backlogTree('sub content 2')])


if __name__ == '__main__':
    import unittest
    unittest.main()

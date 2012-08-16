import myTestCase
import backlogTree

class testBacklogTree(myTestCase.myTestCase):
    def my_setup(self):
        pass
    
    def my_teardown(self):
        pass

    def test_create_blank_tree(self):
        bt = backlogTree.backlogTree()
        self.assertEqual(bt._content, '')
        self.assertEqual(bt._subTree, [])
        self.assertEqual(bt._attribute, backlogTree.backlogTree.defaultAttr)
        
    def test_create_one_node_tree(self):
        bt = backlogTree.backlogTree('root node', [], {'priority':2})
        self.assertEqual(bt._content, 'root node')
        self.assertEqual(bt._subTree, [])
        self.assertEqual(bt._attribute, {'priority':2})
        
    def test_init_blank_tree_from_file(self):
        fileName = 'a backlog'
        testFileContent = ['sub content 1\n', 'sub content 2\n']
        defaultAttr = backlogTree.backlogTree.defaultAttr
        self.mock_function(backlogTree.my_open).with_param(fileName).and_return(testFileContent)
        bt = backlogTree.backlogTree()
        bt.init_from_file(fileName)
        self.assertEqual(fileName, bt._content)
        self.assertEqual(bt._attribute, defaultAttr)
        self.assertEqual(bt._subTree, [backlogTree.backlogTree('sub content 1', [], defaultAttr),
                                       backlogTree.backlogTree('sub content 2', [], defaultAttr)])

    def test_init_one_node_tree_from_file(self):
        fileName = 'a backlog'
        testFileContent = ['sub content 1\n', 'sub content 2\n']
        self.mock_function(backlogTree.my_open).with_param(fileName).and_return(testFileContent)
        bt = backlogTree.backlogTree('root node', [], {'priority':2})
        bt.init_from_file(fileName)
        self.assertEqual('root node', bt._content)
        self.assertEqual({'priority':2}, bt._attribute)
        self.assertEqual(bt._subTree, [backlogTree.backlogTree('sub content 1', [], {'priority':2}),
                                       backlogTree.backlogTree('sub content 2', [], {'priority':2})])
        
if __name__ == '__main__':
    import unittest
    unittest.main()

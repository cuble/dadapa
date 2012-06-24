#! /usr/bin/env python

import unittest

from sprint import sprintDoc
from sprint import sprintDir
from sprint import sprint_main
from sprint import helpString 

from sprintStub import sprintDocStub
from sprintStub import sprintDirStub
from sprintStub import osStub
from sprintStub import fileIoStub

import sys
from cStringIO import StringIO

class SprintDocTests(unittest.TestCase):
    def setUp(self):
        osStub.install()
        fileIoStub.install()

    def tearDown(self):
        osStub.uninstall()
        fileIoStub.uninstall()
        
    def test_doc_notexist(self):
        doc = sprintDoc('123')
        self.assertEqual('unavailable', doc.check())
        
    def _exist_doc_test(self, fname, filestate):
        doc = sprintDoc(fname)
        self.assertEqual(filestate, doc.check())
    
    def test_check_exist_unknown_doc(self):
        fileIoStub.set_exist_file('123', [])
        self._exist_doc_test('123', 'undefined')
        
    def test_check_exist_backlog(self):
        fileIoStub.set_exist_file('sprint_backlog', ['Committed Items:\n','\n',\
                                                     'Not Committed Items:\n', '\n'])
        self._exist_doc_test('sprint_backlog', 'new')
        
    def test_check_exist_review(self):
        fileIoStub.set_exist_file('sprint_review', ['Achievements:\n','\n',\
                                                    'Not Done Items:\n','\n'])
        self._exist_doc_test('sprint_review', 'new')
        
    def test_check_exist_worked_backlog(self):
        fileIoStub.set_exist_file('sprint_backlog', ['Committed Items\n','\n'])
        self._exist_doc_test('sprint_backlog', 'worked')

    def test_initialize_unknown_doc(self):
        self.doc = sprintDoc('123')
        self.assertRaises(NameError, self.doc.initialize)

    def _initialize_doc_test(self, fname):
        self.doc = sprintDoc(fname)
        self.doc.initialize()
        fileIoStub.check_created_files(fname, sprintDoc.templates[fname])

    def test_initialize_backlog(self):
        self._initialize_doc_test('sprint_backlog')
        
    def test_initialize_review(self):
        self._initialize_doc_test('sprint_review')       
        
class SprintDirTests(unittest.TestCase):
    def _new_sprintDir(self, sprintNum):
        self.testIdx = sprintNum
        self.sprintName = sprintDir.prefix + str(sprintNum)
        sprintDocStub.set_expected_check_dir(self.sprintName)
        self.sprint = sprintDir(sprintNum)
        
        self.assertEqual(self.sprintName, self.sprint.getname())
        sprintDocStub.check_objs_created_result(sprintDir.fileList)

    def _init_test_data(self, sprintNum, isDirExist=False):
        self._new_sprintDir(sprintNum)
        if isDirExist: osStub.set_created_dir_list(self.sprintName)

    def _do_check(self, state):
        self.sprint.check()
        stateStr="The state of "+self.sprintName+' is: '+state+'\n'
        self.assertEqual(stateStr, sys.stdout.getvalue())
        self.assertEqual("", osStub.curDir)

    def setUp(self):
        sprintDocStub.install()
        osStub.install()
        self.org_output = sys.stdout
        sys.stdout = StringIO()
        
    def tearDown(self):
        sprintDocStub.check_checked_time(self.assertEqual)
        sprintDocStub.uninstall()
        osStub.uninstall()
        sys.stdout = self.org_output

    def test_check_not_exist(self):
        self._init_test_data(0)
        self._do_check("unavailable")

    def test_check_exist_empty(self):
        self._init_test_data(1, True)
        sprintDocStub.set_expected_check_result('unavailable')
        self._do_check('undefined')
        
    def test_check_exist_new_sprint(self):
        self._init_test_data(1, True)
        sprintDocStub.set_expected_check_result('new', 'new')
        self._do_check('new')

    def test_check_exist_wrong(self):
        self._init_test_data(1, True)
        sprintDocStub.set_expected_check_result('undefined')
        self._do_check('undefined')
        
    def test_check_exist_worked_sprint(self):
        self._init_test_data(2,True)
        sprintDocStub.set_expected_check_result('worked')
        self._do_check('worked')

    def _do_initialize(self, sprintNum=0):
        self._init_test_data(sprintNum, False)
        self.sprint.initialize()
        osStub.check_dir_created(self.sprintName)
        sprintDocStub.check_initialized_result(sprintDir.fileList)
        self.assertEqual("", osStub.curDir)

    def test_initialize(self):
        self._do_initialize()
        
    def test_initialize_another(self):
        self._do_initialize(1)

    def test_initialize_exist_new_sprint(self):
        self._init_test_data(10, True)
        self.sprint.initialize()
        osStub.check_dir_created(self.sprintName)
        self.assertEqual(self.sprintName+" exist, can't be initialized\n", \
                         sys.stdout.getvalue())
        sprintDocStub.check_initialized_result([])
        self.assertEqual("", osStub.curDir)
        
    def _get_last_num_test(self, expected_ret, *existDirs):
        osStub.set_created_dir_list(*existDirs)
        self.assertEqual(expected_ret, sprintDir.get_last_num())
        osStub.check_dir_created(*existDirs)
                
    def test_get_last_num(self):
        self._get_last_num_test(0, '123')
        
    def test_get_last_num_with_one_exist(self):
        self._get_last_num_test(1, 'Sprint-0')
        
    def test_get_last_num_with_two_exist(self):
        self._get_last_num_test(2, 'Sprint-1', 'Sprint-0')
        
    def test_get_last_num_with_miss_ones(self):
        self._get_last_num_test(10, 'Sprint-9', 'Sprint-1')

class SprintMainTest(unittest.TestCase):
    def setUp(self):
        sprintDirStub.install()
        sys.argv = ['-']
        self.org_output = sys.stdout
        sys.stdout = StringIO()
        
    def tearDown(self):
        sprintDirStub.uninstall()
        sys.stdout = self.org_output
        
    def test_print_help_if_no_param(self):
        sprint_main()
        sprintDirStub.check_objs_created()
        sprintDirStub.check_called()
        self.assertEqual(helpString+'\n', sys.stdout.getvalue())
        
    def test_print_help_if_param_error(self):
        sys.argv.append('haha')
        sprint_main()
        sprintDirStub.check_objs_created()
        sprintDirStub.check_called()
        self.assertEqual(helpString+'\n', sys.stdout.getvalue())
               
    def _sprint_main_test(self, *argvs):
        length = len(argvs)
        for index in range(length):
            sys.argv.append(argvs[index])
        sprint_main()
        if argvs[0] == 'new': sprintDirStub.check_called('initialize')
        else: sprintDirStub.check_called(argvs[0])
        if length > 1:
            sprintDirStub.check_objs_created(argvs[1])

    def test_check_sprint(self):
        self._sprint_main_test('check', '1')
        
    def test_check_another_sprint(self):
        self._sprint_main_test('check', '2')
        
    def test_intialize_sprint(self):
        self._sprint_main_test('initialize', '1')
        
    def _param_error_test(self, operation):
        sys.argv.append(operation)
        sprint_main()
        sprintDirStub.check_called()
        self.assertEqual(helpString+'\n', sys.stdout.getvalue())

    def test_initialize_param_error(self):
        self._param_error_test('initialize')
        
    def test_check_param_error(self):
        self._param_error_test('check')
        
    def _sprint_main_with_get_last_num(self, operation, sprintNum):
        sprintDirStub.set_expected_last_num(sprintNum)
        self._sprint_main_test(operation)
        sprintDirStub.check_objs_created(sprintNum+1)
        
    def test_new_sprint(self):
        self._sprint_main_with_get_last_num('new', 1)
        
    def test_new_another_sprint(self):
        self._sprint_main_with_get_last_num('new', 2)
        
    def test_delete_sprint(self):
        self._sprint_main_with_get_last_num('delete', 1)
        
    def test_delete_selected_sprint(self):
        self._sprint_main_test('delete', 2)
        sprintDirStub.check_objs_created(2)


def main():
    unittest.main()

if __name__ == "__main__":
    main()

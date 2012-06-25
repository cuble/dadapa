#! /usr/bin/env python

import unittest
import sys

from sprint import sprintDoc
from sprint import sprintDir
from sprint import sprint_main
from sprint import helpString 

from sprintStub import sprintDocStub
from sprintStub import sprintDirStub
from sprintStub import osStub
from sprintStub import fileIoStub
from sprintStub import sysOutputStub
        
class SprintDocTests(unittest.TestCase):
    def setUp(self):
        osStub.install()
        fileIoStub.install()
        sysOutputStub.install()

    def tearDown(self):
        osStub.uninstall()
        fileIoStub.uninstall()
        sysOutputStub.uninstall()
        
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
        sysOutputStub.check_sys_output("- "+fname+" created\n")

    def test_initialize_backlog(self):
        self._initialize_doc_test('sprint_backlog')
        
    def test_initialize_review(self):
        self._initialize_doc_test('sprint_review')       
        
class SprintDirTests(unittest.TestCase):
    def setUp(self):
        sprintDocStub.install()
        osStub.install()
        sysOutputStub.install()
        
    def tearDown(self):
        sprintDocStub.uninstall()
        osStub.uninstall()
        sysOutputStub.uninstall()

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
        stateStr=self.sprintName+' is: '+state+'\n'
        sysOutputStub.check_sys_output(stateStr)
        self.assertEqual("", osStub.curDir)

    def test_check_not_exist(self):
        self._init_test_data(0)
        self._do_check("unavailable")

    def test_check_exist_empty(self):
        self._init_test_data(1, True)
        sprintDocStub.set_expected_check_result('unavailable', 'unavailable')
        self._do_check('new')
        sprintDocStub.check_initialized_result(sprintDir.fileList)
        
    def test_check_exist_new_sprint(self):
        self._init_test_data(1, True)
        sprintDocStub.set_expected_check_result('new', 'new')
        self._do_check('new')
        sprintDocStub.check_initialized_result([])

    def test_check_exist_wrong(self):
        self._init_test_data(1, True)
        sprintDocStub.set_expected_check_result('undefined')
        self._do_check('undefined')
        sprintDocStub.check_initialized_result([])
        
    def test_check_exist_worked_sprint(self):
        self._init_test_data(2,True)
        sprintDocStub.set_expected_check_result('worked', 'worked')
        self._do_check('worked')
        sprintDocStub.check_initialized_result([])

    def test_check_exist_worked_sprint_with_first_file_missed(self):
        self._init_test_data(1000, True)
        sprintDocStub.set_expected_check_result('unavailable', 'worked')
        self._do_check('worked')
        sprintDocStub.check_initialized_result([sprintDir.fileList[0]])

    def test_check_exist_worked_sprint_with_second_file_missed(self):
        self._init_test_data(1001, True)
        sprintDocStub.set_expected_check_result('worked', 'unavailable')
        self._do_check('worked')
        sprintDocStub.check_initialized_result([sprintDir.fileList[1]])

    def _do_initialize(self, sprintNum=0):
        self._init_test_data(sprintNum, False)
        self.sprint.initialize()
        osStub.check_dir_created(self.sprintName)
        sysOutputStub.check_sys_output(self.sprintName + " created\n")
        sprintDocStub.check_initialized_result(sprintDir.fileList)
        self.assertEqual("", osStub.curDir)

    def test_initialize(self):
        self._do_initialize()
        
    def test_initialize_another(self):
        self._do_initialize(1)

    def test_initialize_exist_sprint(self):
        self._init_test_data(10, True)
        self.sprint.initialize()
        osStub.check_dir_created(self.sprintName)
        sysOutputStub.check_sys_output(self.sprintName+" exist, can't be initialized\n")
        sprintDocStub.check_initialized_result([])
        self.assertEqual("", osStub.curDir)
        
    def _get_last_num_test(self, expected_ret, *existDirs):
        osStub.set_created_dir_list(*existDirs)
        self.assertEqual(expected_ret, sprintDir.get_last_num())
        osStub.check_dir_created(*existDirs)

    def test_get_last_num_in_empty(self):
        self._get_last_num_test(0)
                        
    def test_get_last_num(self):
        self._get_last_num_test(0, '123')
        
    def test_get_last_num_with_one_exist(self):
        self._get_last_num_test(0, 'Sprint-0')
        
    def test_get_last_num_with_two_exist(self):
        self._get_last_num_test(1, 'Sprint-1', 'Sprint-0')
        
    def test_get_last_num_with_miss_ones(self):
        self._get_last_num_test(9, 'Sprint-9', 'Sprint-1')
        
    def test_get_last_num_with_confusing_file(self):
        fileIoStub.set_exist_file('Sprint-101', [])
        self._get_last_num_test(100, 'Sprint-1', '123','Sprint-100')
       
    def test_delete_new_sprint(self):
        self._init_test_data(1, True)
        sprintDocStub.set_expected_check_result('new', 'new')
        self.sprint.delete()
        osStub.check_rmtree_called(self.sprintName)
        sysOutputStub.check_sys_output("{0} is: new\n{0} deleted\n".format(self.sprintName))
        
    def test_delete_not_exist_sprint(self):
        self._init_test_data(0)
        self.sprint.delete()
        osStub.check_rmtree_called("")
        sysOutputStub.check_sys_output("{0} is: unavailable\n".format(self.sprintName))
        
    def test_delete_worked_sprint(self):
        self._init_test_data(4, True)
        sprintDocStub.set_expected_check_result('worked', 'unavailable')
        self.sprint.delete()
        osStub.check_rmtree_called('')
        sprintDocStub.check_initialized_result([])
        sysOutputStub.check_sys_output("{0} is: worked\nDelete FORBIDDEN!\n".format(self.sprintName))

    def test_delete_empty_sprint(self):
        self._init_test_data(4, True)
        sprintDocStub.set_expected_check_result('unavailable', 'unavailable')
        self.sprint.delete()
        osStub.check_rmtree_called(self.sprintName)
        sprintDocStub.check_initialized_result([])
        sysOutputStub.check_sys_output("{0} is: new\n{0} deleted\n".format(self.sprintName))

class SprintMainTest(unittest.TestCase):
    def setUp(self):
        sprintDirStub.install()
        sys.argv = ['-']
        sysOutputStub.install()
        
    def tearDown(self):
        sprintDirStub.uninstall()
        sysOutputStub.uninstall()
        
    def _print_help_check(self):
        sprint_main()
        sprintDirStub.check_objs_created()
        sprintDirStub.check_called()
        sysOutputStub.check_sys_output(helpString+'\n')
        
    def test_print_help_if_no_param(self):
        self._print_help_check()
        
    def test_print_help_if_param_error(self):
        sys.argv.append('haha')
        self._print_help_check()
               
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
        self._print_help_check()

    def test_initialize_param_error(self):
        self._param_error_test('initialize')
        
    def test_check_param_error(self):
        self._param_error_test('check')
        
    def test_new_param_error(self):
        sys.argv.append('new')
        sys.argv.append('1')
        self._print_help_check()
        
    def _sprint_main_with_get_last_num(self, operation, sprintNum):
        sprintDirStub.set_expected_last_num(sprintNum)
        self._sprint_main_test(operation)
        if 'new' == operation: sprintNum = sprintNum + 1
        sprintDirStub.check_objs_created(sprintNum)
        
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

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
        self.doc = sprintDoc('123')
        osStub.set_expected_isfile_result('123', False)
        self.assertEqual('unavailable', self.doc.check())
        
    def _exist_doc_test(self, fname, filestate):
        self.doc = sprintDoc(fname)
        osStub.set_expected_isfile_result(fname, True)
        self.assertEqual(filestate, self.doc.check())
    
    def test_check_exist_unknown_doc(self):
        self._exist_doc_test('123', 'undefined')
        
    def test_check_exist_backlog(self):
        self._exist_doc_test('sprint_backlog', 'new')
        
    def test_check_exist_review(self):
        self._exist_doc_test('sprint_review', 'new')

    def test_initialize_unknown_doc(self):
        self.doc = sprintDoc('123')
        self.assertRaises(NameError, self.doc.initialize)

    def _initialize_doc_test(self, fname):
        self.doc = sprintDoc(fname)
        fileIoStub.set_expected_open(fname, 'w+')
        self.doc.initialize()
        fileIoStub.check_created_files(fname, [])

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
        self.assertEqual(sprintDir.fileList, sprintDocStub.createdList)
        sprintDocStub.check_objs_created_result(sprintDir.fileList)

    def _init_test_data(self, sprintNum, isDirExist):
        self._new_sprintDir(sprintNum)
        osStub.set_expected_isdir_result(self.sprintName, isDirExist)

    def _do_check(self, state):
        self.assertEqual(state, self.sprint.check())
        self.assertEqual("", osStub.curDir, "check should not change cur dir")

    def setUp(self):
        sprintDocStub.install()
        osStub.install()
        
    def tearDown(self):
        sprintDocStub.check_checked_time(self.assertEqual)
        sprintDocStub.uninstall()
        osStub.uninstall()

    def test_check_not_exist(self):
        self._init_test_data(0, False)
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

    def _do_initialize(self, sprintNum=0):
        self._init_test_data(sprintNum, False)
        self.sprint.initialize()
        osStub.check_dir_created(self.sprintName)
        sprintDocStub.check_initialized_result(sprintDir.fileList)

    def test_initialize(self):
        self._do_initialize()
        
    def test_initialize_another(self):
        self._do_initialize(1)



class SprintMainTest(unittest.TestCase):
    def setUp(self):
        sprintDirStub.install()
        sys.argv = ['-']
        self.org_output = sys.stdout
        sys.stdout = StringIO()
        
    def tearDown(self):
        sprintDirStub.uninstall()
        sys.stdout = self.org_output
        
    def _sprint_main_test(self, *argvs):
        length = len(argvs)
        for index in range(length):
            sys.argv.append(argvs[index])
        sprint_main()
        sprintDirStub.check_called(argvs[0])
        sprintDirStub.check_objs_created(argvs[1])

        
    def test_print_help_if_no_param(self):
        sprint_main()
        sprintDirStub.check_objs_created()
        sprintDirStub.check_called()
        self.assertEqual(helpString+'\n', sys.stdout.getvalue())
               
    def test_check_sprint(self):
        self._sprint_main_test('check', '1')
        
    def test_check_another_sprint(self):
        self._sprint_main_test('check', '2')
        
    def test_intialize_sprint(self):
        self._sprint_main_test('initialize', '1')


def main():
    unittest.main()

if __name__ == "__main__":
    main()

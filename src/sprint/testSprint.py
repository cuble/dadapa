#! /usr/bin/env python
import unittest

from sprint import sprintDoc
from sprint import sprintDir
from sprint import sprint_main

from sprintStub import sprintDocStub
from sprintStub import osStub

import os # will be removed after stub done

class SprintDocTests(unittest.TestCase):
    def setUp(self):
        self.dirBeforeTest = os.listdir('.')
        self.curdir = os.getcwd()

    def tearDown(self):
        self.assertEqual(self.curdir, os.getcwd(), "pwd change not allowed")
        self.assertEqual(self.dirBeforeTest, os.listdir('.'), "files change not allowed")

    def test_doc_notexist(self):
        self.doc = sprintDoc('123')
        self.assertEqual('unavailable', self.doc.check())
        
    def test_initialize_unknown_doc(self):
        self.doc = sprintDoc('123')
        self.assertRaises(NameError, self.doc.initialize)

    def _initialize_doc_test(self, fname, filestate):
        self.doc = sprintDoc(fname)
        self.doc.initialize()
        self.assertEqual(filestate, self.doc.check())
        self.assertTrue(os.path.isfile(self.doc._sprintDoc__name))
        os.remove(self.doc._sprintDoc__name)

    def test_initialize_backlog(self):
        self._initialize_doc_test('sprint_backlog', 'new')
        
    def test_initialize_review(self):
        self._initialize_doc_test('sprint_review', 'new')
        
    def _exist_doc_test(self, fname, filestate):
        self.doc = sprintDoc(fname)
        f = open(fname, 'w+')
        f.close()
        self.assertEqual(filestate, self.doc.check())
        os.remove(fname)
    
    def test_check_exist_unknown_doc(self):
        self._exist_doc_test('123', 'undefined')
        
    def test_check_exist_backlog(self):
        self._exist_doc_test('sprint_backlog', 'new')
        
    def test_check_exist_review(self):
        self._exist_doc_test('sprint_review', 'new')

        
class SprintDirTests(unittest.TestCase):
    def _new_sprintDir(self, sprintNum):
        self.testIdx = sprintNum
        self.sprint = sprintDir(sprintNum)
        self.sprintName = sprintDir.prefix + str(sprintNum)
        self.assertEqual(self.sprintName, self.sprint.getname())
        self.assertEqual(sprintDir.fileList, sprintDocStub.createdList)
        sprintDocStub.check_created_result(self.assertEqual, sprintDir.fileList)

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
        sprintDocStub.set_expected_check_result(self.sprintName, 'unavailable')
        self._do_check('undefined')
        
    def test_check_exist_new_sprint(self):
        self._init_test_data(1, True)
        sprintDocStub.set_expected_check_result(self.sprintName, 'new', 'new')
        self._do_check('new')

    def test_check_exist_wrong(self):
        self._init_test_data(1, True)
        sprintDocStub.set_expected_check_result(self.sprintName, 'undefined')
        self._do_check('undefined')

    def _do_initialize(self, sprintNum=0):
        self._init_test_data(sprintNum, False)
        self.sprint.initialize()
        osStub.check_dir_created(self.assertEqual, self.sprintName)
        sprintDocStub.check_initialized_result(self.assertEqual, sprintDir.fileList)

    def test_initialize(self):
        self._do_initialize()
        
    def test_initialize_another(self):
        self._do_initialize(1)


class SprintMainTest(unittest.TestCase):        
    def test_main(self):
        sprint_main()

def main():
    unittest.main()

if __name__ == "__main__":
    main()

#! /usr/bin/env python
from sprint import *
import unittest

class SprintDocTests(unittest.TestCase):
    def setUp(self):
        self.dirBeforeTest=os.listdir('.')
        self.curdir=os.getcwd()

    def tearDown(self):
        self.assertEqual(self.curdir,os.getcwd(),"pwd change not allowed")
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

def init_stub(self, fname):
    sprintDocStub.createdList.append(fname)
    
def clear_stub():
    sprintDocStub.createdList = []
    
def initialize_stub(self):
    pass

def check_stub(self):
    result = sprintDocStub.checkReturnVal[sprintDocStub.checkCalledTime]
    sprintDocStub.checkCalledTime = sprintDocStub.checkCalledTime + 1
    return result

class sprintDocStub:
    createdList = []
    orig_init=sprintDoc.__init__
    orig_initialize = sprintDoc.initialize
    orig_check = sprintDoc.check
    checkReturnVal = ()
    checkExpectedCallTime = 0
    checkCalledTime = 0

    @classmethod
    def install(self):
        sprintDoc.__init__ = init_stub
        sprintDoc.initialize = initialize_stub
        sprintDoc.check = check_stub
        self.clear()
        
    @classmethod
    def check_init_result(self, desire):
        return (desire == self.createdList)

    @classmethod
    def clear(self):
        self.createdList=[]
        self.checkExpectedCallTime = 0
        self.checkCalledTime = 0

    @classmethod
    def uninstall(self):
        sprintDoc.__init__ = self.orig_init
        sprintDoc.initialize = self.orig_initialize
        sprintDoc.check = self.orig_check
        
    @classmethod
    def set_expected_check_result(self, *val):
        self.checkExpectedCallTime = len(val)
        self.checkReturnVal = val
        
    @classmethod
    def check_checked_time(self, func):
        func(self.checkExpectedCallTime, self.checkCalledTime)
        
class SprintDirTests(unittest.TestCase):
    def _create_test_sprint(self, dirname, status):
        os.mkdir(dirname)
        if status == 'CreateNew': 
            sprintDocStub.set_expected_check_result('new','new')
        elif status == 'CreateEmpty': 
            sprintDocStub.set_expected_check_result('unavailable')
        elif status == 'CreateWrong': 
            sprintDocStub.set_expected_check_result('undefined')

    def _init_test_data(self, n, createType=''):
        self.testIdx=n
        self.sprint=sprintDir(n)
        if createType != '': self._create_test_sprint(self.sprint.getname(), createType)

    def setUp(self):
        sprintDocStub.install()
        self.dirBeforeTest=os.listdir('.')
        self.curdir=os.getcwd()
        
    def tearDown(self):
        sprintDocStub.check_checked_time(self.assertEqual)
        sprintDocStub.uninstall()
        if(os.path.isdir(self.sprint.getname())): shutil.rmtree(self.sprint.getname())
        self.assertEqual(self.curdir,os.getcwd(),"pwd change not allowed")
        self.assertEqual(self.dirBeforeTest, os.listdir('.'), "files change not allowed")

    def test_check_not_exist(self):
        self._init_test_data(0)
        self.assertEqual("unavailable",self.sprint.check())
        self.assertEqual(sprintDir.fileList, sprintDocStub.createdList)
        
    def _create_new_check(self, n=0):
        self._init_test_data(n)
        sprintDocStub.set_expected_check_result('new','new')
        self.sprint.initialize()
        self.assertEqual(SprintDirPrefix+str(self.testIdx), self.sprint.getname())
        self.assertTrue(os.path.isdir(self.sprint.getname()))
        self.assertTrue(sprintDocStub.check_init_result(sprintDir.fileList))
        self.assertEqual('new', self.sprint.check())

    def test_create_new(self):
        self._create_new_check()
        
    def test_create_another(self):
        self._create_new_check(1)

    def test_check_exist_new_sprint(self):
        self._init_test_data(1,'CreateNew')
        self.assertEqual('new', self.sprint.check())

    def test_check_exist_empty(self):
        self._init_test_data(1,'CreateEmpty')
        self.assertEqual('undefined', self.sprint.check())
        
    def test_check_exist_wrong(self):
        self._init_test_data(1, 'CreateWrong')
        self.assertEqual('undefined', self.sprint.check())

class SprintMainTest(unittest.TestCase):        
    def test_main(self):
        sprint_main()

def main():
    unittest.main()

if __name__ == "__main__":
    main()

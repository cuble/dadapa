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
    pass

class sprintDocStub:
    createdList = []
    def __init__(self, fname):
        #print "stub called"
        self.createdList.append(fname)
        pass

        
    def clear(self):
        self.createdList=[]

    def set_state(self, state):
        pass
        
class SprintDirTests(unittest.TestCase):
    def _attach_file(self, sprint, fname, state='new'):
        # os.chdir(sprint.getname())
        doc=sprintDocStub(fname)
        doc.set_state('new')
        sprint._sprintDir__docs.append(doc)
        # os.chdir('..')

    def _create_test_sprint(self, dirname, status):
        os.mkdir(dirname)
        if status == 'CreateNew': 
            self._attach_file(self.sprint, 'sprint_backlog')
            f=open(dirname+'/sprint_backlog', 'w+')
            f.close()
            f=open(dirname+'/sprint_review', 'w+')
            f.close()
        elif status == 'CreateEmpty': pass
        elif status == 'CreateWrong': 
            self._attach_file(self.sprint, '123')
            # f=open(dirname+'/123', 'w+')
            # f.close()

    def _init_test_data(self, n, createType=''):
        self.testIdx=n
        self.sprint=sprintDir(n)
        if createType != '': self._create_test_sprint(self.sprint.getname(), createType)

    def _set_sprintDoc_stub(self):
        self.orig_init=sprintDoc.__init__ 
        self.orig_initialize=sprintDoc.initialize
        sprintDoc.__init__ = init_stub
        sprintDoc.initialize=initialize_stub

    def setUp(self):
        self._set_sprintDoc_stub()
        self.dirBeforeTest=os.listdir('.')
        self.curdir=os.getcwd()

    def _clear_sprintDoc_stub(self):
        sprintDoc.__init__ = self.orig_init
        sprintDoc.initialize = self.orig_initialize
        clear_stub()
        
    def tearDown(self):
        self._clear_sprintDoc_stub()
        if(os.path.isdir(self.sprint.getname())): shutil.rmtree(self.sprint.getname())
        self.assertEqual(self.curdir,os.getcwd(),"pwd change not allowed")
        self.assertEqual(self.dirBeforeTest, os.listdir('.'), "files change not allowed")

    def test_check_not_exist(self):
        self._init_test_data(0)
        self.assertEqual("unavailable",self.sprint.check())
        self.assertEqual(sprintDir.fileList, sprintDocStub.createdList)
        
    def _create_new_check(self, n=0):
        self._init_test_data(n)
        self.sprint.initialize()
        self.assertEqual(SprintDirPrefix+str(self.testIdx), self.sprint.getname())
        self.assertTrue(os.path.isdir(self.sprint.getname()))
        self.assertEqual('new', self.sprint.check())
        self.assertEqual(sprintDir.fileList, sprintDocStub.createdList)

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

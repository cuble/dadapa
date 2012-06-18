#! /usr/bin/env python
import os
from os import system
import shutil


SprintDirPrefix='Sprint-'
class sprintDir:
    fileList=['sprint_backlog', 'sprint_review']
    def __init__(self, n):
        self.__name=SprintDirPrefix+str(n)
        self.__state = 'unavailable'
        self.__docs = []
        
    def getname(self):
        return self.__name
        
    def check(self):
        if os.path.isdir(self.__name): 
            self.__state='new'
            for filename in self.fileList:
                if filename not in os.listdir(self.__name): 
                    self.__state='undefined'
        return self.__state
        
    def initialize(self):
        os.mkdir(self.__name)
        os.chdir(self.__name)
        for fname in self.fileList: 
            f=open(fname, 'w+')
            f.close()
        os.chdir('..')
        pass

class sprintDoc:
    def __init__(self, fname):
        self.__name = fname
        pass
        
    def check(self):
        if not os.path.isfile(self.__name): return 'unavailable'
        if self.__name not in sprintDir.fileList: return 'undefined'
        return 'new'
        
    def initialize(self):
        if self.__name not in sprintDir.fileList: raise NameError(self.__name)
        f=open(self.__name, 'w+')
        f.close()

# Test cases        
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

class sprintDocStub:
    def __init__(self, fname):
        pass

    def set_state(self, state):
        pass
        
class SprintDirTests(unittest.TestCase):
    def _attach_file(self, sprint, fname, state='new'):
        # os.chdir(sprint.getname())
        doc=sprintDocStub(fname)
        doc.set_state('new')
        sprint._sprintDir__docs.append(doc)
        # os.chdir('..')

    def _createTestSprint(self, dirname, status):
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

    def _initTestData(self, n, createType=''):
        self.testIdx=n
        self.sprint=sprintDir(self.testIdx)
        if createType != '': self._createTestSprint(self.sprint.getname(), createType)

    def setUp(self):
        self._initTestData(0)
        self.dirBeforeTest=os.listdir('.')
        self.curdir=os.getcwd()

    def tearDown(self):
        if(os.path.isdir(self.sprint.getname())): shutil.rmtree(self.sprint.getname())
        self.assertEqual(self.curdir,os.getcwd(),"pwd change not allowed")
        self.assertEqual(self.dirBeforeTest, os.listdir('.'), "files change not allowed")

    def testCheckNotexist(self):
        self.assertEqual("unavailable",self.sprint.check())
        
    def _createNewCheck(self, n=0):
        self._initTestData(n)
        self.sprint.initialize()
        self.assertEqual(SprintDirPrefix+str(self.testIdx), self.sprint.getname())
        self.assertTrue(os.path.isdir(self.sprint.getname()))
        self.assertEqual('new', self.sprint.check())
        self.assertEqual(self.sprint.fileList, os.listdir(self.sprint.getname()))
        
    def testCreateNew(self):
        self._createNewCheck()
        
    def testCreateAnother(self):
        self._createNewCheck(1)

    def testCheckExistNewSprint(self):
        self._initTestData(1,'CreateNew')
        self.assertEqual('new', self.sprint.check())

    def testCheckExistEmpty(self):
        self._initTestData(1,'CreateEmpty')
        self.assertEqual('undefined', self.sprint.check())
        
    def testCheckExitWrong(self):
        self._initTestData(1, 'CreateWrong')
        self.assertEqual('undefined', self.sprint.check())
        

def main():
    unittest.main()

if __name__ == "__main__":
    main()

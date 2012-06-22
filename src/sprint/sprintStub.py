#! /usr/bin/env python

import os
from sprint import sprintDoc
from sprint import sprintDir

def assert_equal(expected, actual):
    assert expected == actual, "%s, %s" %(str(expected), str(actual))

class sprintDocStub:
    createdList = []
    initializedList = []
    org_init = sprintDoc.__init__
    org_initialize = sprintDoc.initialize
    org_check = sprintDoc.check
    expectedCheckReturnVal = ()
    expectedCheckCallTime = 0
    checkCalledTime = 0
    expectedCheckDir = ""
    initialize_called_time = 0

    @classmethod
    def install(cls):
        sprintDoc.__init__ = init_stub
        sprintDoc.initialize = initialize_stub
        sprintDoc.check = check_stub
        cls.clear()
        
    @classmethod
    def check_objs_created_result(cls, desire):
        assert_equal(desire, cls.createdList)
    
    @classmethod
    def check_initialized_result(cls, desired):
        assert_equal(desired, cls.initializedList)

    @classmethod
    def clear(cls):
        cls.createdList = []
        cls.initializedList = []
        cls.expectedCheckCallTime = 0
        cls.checkCalledTime = 0
        cls.expectedCheckDir = ""
        cls.initialize_called_time = 0

    @classmethod
    def uninstall(cls):
        sprintDoc.__init__ = cls.org_init
        sprintDoc.initialize = cls.org_initialize
        sprintDoc.check = cls.org_check
        
    @classmethod
    def set_expected_check_dir(cls, checkDir):
        cls.expectedCheckDir = checkDir
        
    @classmethod
    def set_expected_check_result(cls, *val):
        cls.expectedCheckCallTime = len(val)
        cls.expectedCheckReturnVal = val
        
    @classmethod
    def check_checked_time(cls, func):
        func(cls.expectedCheckCallTime, cls.checkCalledTime)

def init_stub(self, fname):
    sprintDocStub.createdList.append(fname)
    
def initialize_stub(self):
    assert_equal(osStub.curDir, sprintDocStub.expectedCheckDir)
    sprintDocStub.initializedList.append(sprintDocStub.createdList[sprintDocStub.initialize_called_time])
    sprintDocStub.initialize_called_time = sprintDocStub.initialize_called_time + 1 

def check_stub(self):
    assert_equal(osStub.curDir, sprintDocStub.expectedCheckDir)
    result = sprintDocStub.expectedCheckReturnVal[sprintDocStub.checkCalledTime]
    sprintDocStub.checkCalledTime = sprintDocStub.checkCalledTime + 1
    return result



class sprintDirStub:
    org_check = sprintDir.check
    org_init = sprintDir.__init__
    org_initialize = sprintDir.initialize
    calledFuncList = []
    objsCreated = []
    @classmethod
    def install(cls):
        sprintDir.check = sprint_check_stub
        sprintDir.__init__ = sprint_init_stub
        sprintDir.initialize = sprint_initialize_stub
        cls.calledFuncList = []
        cls.objsCreated = []
    
    @classmethod
    def uninstall(cls):
        sprintDir.check = cls.org_check
        sprintDir.__init__ = cls.org_init
        sprintDir.initialize = cls.org_initialize
    
    @classmethod
    def check_called(cls, *expectedFuncList):
        length = len(expectedFuncList)
        assert_equal(len(cls.calledFuncList), length)
        for index in range(length):
            assert_equal(cls.calledFuncList[index], expectedFuncList[index])
            
    @classmethod
    def check_objs_created(cls, *expectedObjs):
        length = len(expectedObjs)
        assert_equal(len(cls.objsCreated), length)
        for index in range(length):
            assert_equal(cls.objsCreated[index], expectedObjs[index])
            
def sprint_check_stub(self):
    sprintDirStub.calledFuncList.append("check")
    
def sprint_init_stub(self,sprintNum):
    sprintDirStub.objsCreated.append(sprintNum)
           
def sprint_initialize_stub(self):
    sprintDirStub.calledFuncList.append("initialize")


class osStub:
    org_mkdir = os.mkdir
    org_chdir = os.chdir
    org_isdir = os.path.isdir
    org_isfile = os.path.isfile
    isdirReturnVal = False
    isdirPath = ""
    isfileReturnVal = False
    isfileName = ""
    createdDirList = []
    curDir = ""
    @classmethod
    def install(cls):
        os.mkdir = mkdir_stub
        os.chdir = chdir_stub
        os.path.isdir = isdir_stub
        os.path.isfile = isfile_stub
        cls.clear()

    @classmethod
    def clear(cls):
        cls.isdirReturnVal = False
        cls.isdirPath = ""
        cls.isfileReturnVal = False
        cls.isfileName = ""
        cls.createdDirList = []
        cls.curDir = ""
        
    @classmethod
    def uninstall(cls):
        os.mkdir = cls.org_mkdir
        os.chdir = cls.org_chdir
        os.path.isdir = cls.org_isdir
        os.path.isfile = cls.org_isfile

    @classmethod
    def set_expected_isdir_result(cls, path, ret):
        osStub.curDir = ""
        cls.isdirPath = path
        cls.isdirReturnVal = ret
        
    @classmethod
    def check_dir_created(cls, *dirs):
        length = len(dirs)
        assert_equal(length, len(cls.createdDirList))
        for index in range(length): 
            assert_equal(dirs[index], cls.createdDirList[index])
            
    @classmethod
    def set_expected_isfile_result(cls, name, ret):
        cls.isfileName = name
        cls.isfileReturnVal = ret

def mkdir_stub(path):
    assert_equal(osStub.curDir, "")
    osStub.createdDirList.append(path)

def chdir_stub(path):
    if('..' == path): osStub.curDir = ""
    else: osStub.curDir = path

def isdir_stub(path):
    assert_equal(osStub.curDir, "")
    assert_equal(path, osStub.isdirPath)
    return osStub.isdirReturnVal

def isfile_stub(name):
    assert_equal(osStub.isfileName, name)
    return osStub.isfileReturnVal


class fileIoStub:
    org_open_file = sprintDoc.open_file
    expectedOpenFile = ""
    expectedOpenFlag = ""
    createdFiles = {}
    @classmethod
    def install(cls):
        sprintDoc.open_file = open_stub
        cls.expectedOpenFile = ""
        cls.expectedOpenFlag = ""
        cls. createdFiles = {}
        
    @classmethod
    def uninstall(cls):
        sprintDoc.open_file = cls.org_open_file
    
    @classmethod
    def set_expected_open(cls, fileName, flag):
        cls.expectedOpenFile = fileName
        cls.expectedOpenFlag = flag
        
    @classmethod
    def check_created_files(cls, fname, contents):
        assert_equal(cls.createdFiles[fname], contents)
            
def open_stub(self, fileName, flag):
    assert_equal(fileIoStub.expectedOpenFile, fileName)
    assert_equal(fileIoStub.expectedOpenFlag, flag)
    return fileStub(fileName)
    
class fileStub:
    def __init__(self, name):
        self.name = name
        self.content = []

    def close(self):
        fileIoStub.createdFiles[self.name]=self.content

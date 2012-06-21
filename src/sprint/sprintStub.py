#! /usr/bin/env python
import os
from sprint import sprintDoc

class sprintDocStub:
    createdList = []
    initializedList = []
    orig_init = sprintDoc.__init__
    orig_initialize = sprintDoc.initialize
    orig_check = sprintDoc.check
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
    def check_created_result(cls, assert_equal, desire):
        assert_equal(desire, cls.createdList)
    
    @classmethod
    def check_initialized_result(cls, assert_equal, desired):
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
        sprintDoc.__init__ = cls.orig_init
        sprintDoc.initialize = cls.orig_initialize
        sprintDoc.check = cls.orig_check
        
    @classmethod
    def set_expected_check_result(cls, checkDir, *val):
        cls.expectedCheckDir = checkDir
        cls.expectedCheckCallTime = len(val)
        cls.expectedCheckReturnVal = val
        
    @classmethod
    def check_checked_time(cls, func):
        func(cls.expectedCheckCallTime, cls.checkCalledTime)

def init_stub(self, fname):
    sprintDocStub.createdList.append(fname)
    
def initialize_stub(self):
    assert osStub.curDir == sprintDocStub.expectedCheckDir
    sprintDocStub.initializedList.append(sprintDocStub.createdList[sprintDocStub.initialize_called_time])
    sprintDocStub.initialize_called_time = sprintDocStub.initialize_called_time + 1 

def check_stub(self):
    assert osStub.curDir == sprintDocStub.expectedCheckDir
    result = sprintDocStub.expectedCheckReturnVal[sprintDocStub.checkCalledTime]
    sprintDocStub.checkCalledTime = sprintDocStub.checkCalledTime + 1
    return result


class osStub:
    orig_mkdir = os.mkdir
    orig_isdir = os.path.isdir
    orig_chdir = os.chdir
    isdirReturnVal = False
    isdirPath = ""
    createdDirList = []
    curDir = ""
    @classmethod
    def install(cls):
        os.mkdir = mkdir_stub
        os.path.isdir = isdir_stub
        os.chdir = chdir_stub
        cls.clear()

    @classmethod
    def clear(cls):
        cls.isdirReturnVal = False
        cls.isdirPath = ""
        cls.createdDirList = []
        cls.curDir = ""
        
    @classmethod
    def uninstall(cls):
        os.mkdir = cls.orig_mkdir
        os.path.isdir = cls.orig_isdir
        os.chdir = cls.orig_chdir

    @classmethod
    def set_expected_isdir_result(cls, path, ret):
        osStub.curDir = ""
        cls.isdirPath = path
        cls.isdirReturnVal = ret
        
    @classmethod
    def check_dir_created(cls, assert_equal, *dirs):
        length = len(dirs)
        assert_equal(length, len(cls.createdDirList))
        for index in range(length): 
            assert_equal(dirs[index], cls.createdDirList[index])

def mkdir_stub(path):
    assert osStub.curDir == ""
    osStub.createdDirList.append(path)

def isdir_stub(path):
    assert osStub.curDir == ""
    assert path == osStub.isdirPath
    return osStub.isdirReturnVal

def chdir_stub(path):
    if('..' == path): osStub.curDir = ""
    else: osStub.curDir = path

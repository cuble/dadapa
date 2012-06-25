#! /usr/bin/env python

import os
import shutil
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

    @classmethod
    def uninstall(cls):
        sprintDoc.__init__ = cls.org_init
        sprintDoc.initialize = cls.org_initialize
        sprintDoc.check = cls.org_check
        assert_equal(cls.expectedCheckCallTime, cls.checkCalledTime)
        
    @classmethod
    def set_expected_check_dir(cls, checkDir):
        cls.expectedCheckDir = checkDir
        
    @classmethod
    def set_expected_check_result(cls, *val):
        cls.expectedCheckCallTime = len(val)
        cls.expectedCheckReturnVal = val
                
def init_stub(self, fname):
    sprintDocStub.createdList.append(fname)
    self.name=fname
    
def initialize_stub(self):
    assert_equal(osStub.curDir, sprintDocStub.expectedCheckDir)
    sprintDocStub.initializedList.append(self.name) 

def check_stub(self):
    assert_equal(osStub.curDir, sprintDocStub.expectedCheckDir)
    result = sprintDocStub.expectedCheckReturnVal[sprintDocStub.checkCalledTime]
    sprintDocStub.checkCalledTime = sprintDocStub.checkCalledTime + 1
    return result


class sprintDirStub:
    org_check = sprintDir.check
    org_init = sprintDir.__init__
    org_initialize = sprintDir.initialize
    org_delete = sprintDir.delete
    org_get_last_num = sprintDir.get_last_num
    calledFuncList = []
    objsCreated = []
    expectedLastNum = 0
    @classmethod
    def install(cls):
        sprintDir.check = sprint_check_stub
        sprintDir.__init__ = sprint_init_stub
        sprintDir.initialize = sprint_initialize_stub
        sprintDir.delete = sprint_delete_stub
        sprintDir.get_last_num = classmethod(sprint_get_last_num_stub)
        cls.calledFuncList = []
        cls.objsCreated = []
    
    @classmethod
    def uninstall(cls):
        sprintDir.check = cls.org_check
        sprintDir.__init__ = cls.org_init
        sprintDir.initialize = cls.org_initialize
        sprintDir.get_last_num = cls.org_get_last_num
        
    @classmethod
    def set_expected_last_num(cls, num):
        cls.expectedLastNum = num

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
    
def sprint_delete_stub(self):
    sprintDirStub.calledFuncList.append("delete")

def sprint_get_last_num_stub(cls):
    return sprintDirStub.expectedLastNum

class osStub:
    org_mkdir = os.mkdir
    org_chdir = os.chdir
    org_isdir = os.path.isdir
    org_isfile = os.path.isfile
    org_listdir = os.listdir
    isdirReturnVal = False
    isdirPath = ""
    isfileReturnVal = False
    isfileName = ""
    createdDirList = []
    curDir = ""
    rmed_dir = ""

    @classmethod
    def install(cls):
        os.mkdir = mkdir_stub
        os.chdir = chdir_stub
        os.path.isdir = isdir_stub
        os.path.isfile = isfile_stub
        os.listdir = listdir_stub
        shutil.rmtree = rmtree_stub
        cls.clear()
        fileIoStub.clear()

    @classmethod
    def clear(cls):
        cls.isdirReturnVal = False
        cls.isdirPath = ""
        cls.isfileReturnVal = False
        cls.isfileName = ""
        cls.createdDirList = []
        cls.curDir = ""
        cls.rmed_dir = ""
    @classmethod
    def uninstall(cls):
        os.mkdir = cls.org_mkdir
        os.chdir = cls.org_chdir
        os.listdir = cls.org_listdir
        os.path.isdir = cls.org_isdir
        os.path.isfile = cls.org_isfile
        
    @classmethod
    def check_dir_created(cls, *dirs):
        length = len(dirs)
        assert_equal(length, len(cls.createdDirList))
        for index in range(length): 
            assert_equal(dirs[index], cls.createdDirList[index])
            
    @classmethod
    def set_created_dir_list(cls, *dirs):
        length = len(dirs)
        for index in range(length): 
            cls.createdDirList.append(dirs[index])

    @classmethod
    def check_rmtree_called(cls, path):
        assert_equal(path, cls.rmed_dir)

            
def mkdir_stub(path):
    assert_equal(osStub.curDir, "")
    osStub.createdDirList.append(path)

def chdir_stub(path):
    if '..' == path:
        if osStub.curDir == "": raise NameError(path) 
        else: osStub.curDir = ""
    else: osStub.curDir = path

def isdir_stub(path):
    return (path in osStub.createdDirList)

def isfile_stub(name):
    return name in fileIoStub.createdFiles.keys()

def listdir_stub(path):
    return osStub.createdDirList + fileIoStub.createdFiles.keys()

def rmtree_stub(path):
    osStub.rmed_dir = path

class fileIoStub:
    org_open_file = sprintDoc.open_file
    createdFiles = {}
    
    @classmethod
    def install(cls):
        sprintDoc.open_file = open_stub
        cls.clear()
        
    @classmethod
    def clear(cls):
        cls.expectedOpenFile = ""
        cls.expectedOpenFlag = ""
        cls. createdFiles = {}
                
    @classmethod
    def uninstall(cls):
        sprintDoc.open_file = cls.org_open_file
        
    @classmethod
    def check_created_files(cls, fname, contents):
        assert_equal(cls.createdFiles[fname], contents)
            
    @classmethod
    def set_exist_file(cls, fname, contents):
        cls.createdFiles[fname] = contents
        
def open_stub(self, fileName, flag):
    f = fileStub(fileName)
    if flag == 'w+': pass
    elif flag == 'r': 
        f.writelines(fileIoStub.createdFiles[fileName])
    return f
    
class fileStub:
    def __init__(self, name):
        self.name = name
        self.content = []

    def close(self):
        fileIoStub.createdFiles[self.name]=self.content
        
    def writelines(self, contents):
        self.content = self.content + contents
        
    def __iter__(self):
        return self.content.__iter__()

import sys
from cStringIO import StringIO

class sysOutputStub:
    org_stdout = sys.stdout
    @classmethod
    def install(cls):
        sys.stdout = StringIO()
        
    @classmethod
    def uninstall(cls):
        assert_equal ('', sys.stdout.getvalue())
        sys.stdout = cls.org_stdout
        
    @classmethod
    def check_sys_output(cls, desired_output):
        assert_equal(desired_output, sys.stdout.getvalue())
        sys.stdout = StringIO() #clear the output after check
        
        

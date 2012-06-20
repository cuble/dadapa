#! /usr/bin/env python

from sprint import *

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

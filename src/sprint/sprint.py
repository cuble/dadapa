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
        for f in self.fileList: self.__docs.append(sprintDoc(f))
        
    def getname(self):
        return self.__name
        
    def check(self):
        if os.path.isdir(self.__name): 
            self.__state='new'
            for doc in self.__docs:
                if doc.check() != 'new': 
                    self.__state = 'undefined'
                    break
        return self.__state
        
    def initialize(self):
        os.mkdir(self.__name)
        os.chdir(self.__name)
        for doc in self.__docs:
            doc.initialize()
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

def sprint_main():
    pass

if __name__=='__main__':
    sprint_main()
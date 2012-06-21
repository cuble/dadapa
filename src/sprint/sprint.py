#! /usr/bin/env python
import os

class sprintDir:
    prefix = 'Sprint-'
    fileList = ['sprint_backlog', 'sprint_review']
    def __init__(self, n):
        self.__name = sprintDir.prefix + str(n)
        self.__state = 'unavailable'
        self.__docs = []
        for f in self.fileList: self.__docs.append(sprintDoc(f))
        
    def getname(self):
        return self.__name
        
    def check(self):
        state = 'unavailable'
        if os.path.isdir(self.__name):
            os.chdir(self.__name)
            state = 'new' 
            for doc in self.__docs:
                if doc.check() != 'new': 
                    state = 'undefined'
                    break
        os.chdir("..")
        return state
        
    def initialize(self):
        os.mkdir(self.__name)
        os.chdir(self.__name)
        for doc in self.__docs:
            doc.initialize()
#        os.chdir('..')

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
        f = open(self.__name, 'w+')
        f.close()

def sprint_main():
    pass

if __name__ == '__main__':
    sprint_main()

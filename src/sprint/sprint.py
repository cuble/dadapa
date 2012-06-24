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
                state = doc.check()
                if state == 'unavailable': state='undefined'
                if state != 'new': break
        os.chdir("..")
        print 'The state of {} is: {}'.format(self.__name, state)
        return state
        
    def initialize(self):
        if os.path.isdir(self.__name):
            print "{} exist, can't be initialized".format(self.__name)
        else:
            os.mkdir(self.__name)
            os.chdir(self.__name)
            for doc in self.__docs:
                doc.initialize()
            os.chdir('..')

    def delete(self):
        pass

    @classmethod
    def get_last_num(cls):
        lastSprintNum = 0
        dirList = os.listdir('.')
        for dirName in dirList:
            print dirName
        return lastSprintNum

class sprintDoc:
    templates = {'sprint_backlog': ["Committed Items:\n", 
                                    "\n",
                                    "Not Committed Items:\n",
                                    "\n"],
                 'sprint_review': ["Achievements:\n",
                                   "\n",
                                   "Not Done Items:\n",
                                   "\n"]}
    def __init__(self, fname):
        self.__name = fname
        pass
        
    def check(self):
        if not os.path.isfile(self.__name): return 'unavailable'
        if self.__name not in sprintDir.fileList: return 'undefined'
        f = self.open_file(self.__name, 'r')
        contents = []
        for line in f:
            contents.append(line)
        if contents != self.templates[self.__name]:
            return 'worked'
        return 'new'
        
    def initialize(self):
        if self.__name not in sprintDir.fileList: raise NameError(self.__name)
        f = self.open_file(self.__name, 'w+')
        f.writelines(self.templates[self.__name])
        f.close()
        
    def open_file(self, fname, flag):
        return open(fname, flag)

helpString = """Usage: sprint operation [param]
    sprint new
    sprint delete [1]
    sprint check 1
    sprint initialize 1"""
def sprint_main():
    import sys
    def do_check():
        sprint.check()
        
    def do_initialize():
        sprint.initialize()

    def do_new():
        sprint.initialize()
    
    def do_delete():
        sprint.delete()
        
    def print_help():
        print helpString
        
    cmdTable = {'check': do_check, 'initialize': do_initialize, \
                'new': do_new, 'delete': do_delete}
        
    if len(sys.argv) == 1 or sys.argv[1] not in cmdTable.keys():
        return print_help()
    
    if len(sys.argv) > 2: sprintNum = sys.argv[2]
    elif sys.argv[1] in ['initialize', 'check']: return print_help()
    else: sprintNum = sprintDir.get_last_num() + 1
    sprint = sprintDir(sprintNum)

    cmdTable[sys.argv[1]]()

if __name__ == '__main__':
    sprint_main()

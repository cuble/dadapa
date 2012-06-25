#! /usr/bin/env python

import os
import shutil

class sprintDir:
    prefix = 'Sprint-'
    fileList = ['sprint_backlog', 'sprint_review']
    def __init__(self, n):
        self.__name = sprintDir.prefix + str(n)
        self.__docs = []
        for f in self.fileList: self.__docs.append(sprintDoc(f))
        
    def getname(self):
        return self.__name
        
    def check(self, createMissedFiles=True):
        sprint_state = 'unavailable'
        if os.path.isdir(self.__name):
            sprint_state=state = 'new' 
            os.chdir(self.__name)
            for doc in self.__docs:
                state = doc.check()
                if state == 'unavailable' and createMissedFiles:
                    doc.initialize() 
                elif state == 'worked': 
                    sprint_state = state
                elif state == 'undefined': break
                state = 'new' 
            os.chdir("..")
            if state != 'new': sprint_state = state
        print '{0} is: {1}'.format(self.__name, sprint_state)
        return sprint_state
        
    def initialize(self):
        if os.path.isdir(self.__name):
            print "{0} exist, can't be initialized".format(self.__name)
        else:
            os.mkdir(self.__name)
            print "{0} created".format(self.__name)
            os.chdir(self.__name)
            for doc in self.__docs:
                doc.initialize()
            os.chdir('..')

    def delete(self):
        state = self.check(False)
        if state == 'new':
            shutil.rmtree(self.__name)
            print "{0} deleted".format(self.__name)
        if state == 'worked': print "Delete FORBIDDEN!"

    @classmethod
    def get_last_num(cls):
        lastSprintNum = 0
        dirList = os.listdir('.')
        for dirName in dirList:
            if not os.path.isdir(dirName) or dirName.rfind(sprintDir.prefix) == -1: continue
            sprintNum = dirName[len(sprintDir.prefix):]
            if int(sprintNum) > lastSprintNum: 
                lastSprintNum = int(sprintNum)
        return lastSprintNum

class sprintDoc:
    templates = {'sprint_backlog': ["Period:\n",
                                    "\n",
                                    "Committed Items:\n", 
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
        print "- {0} created".format(self.__name)
        
    def open_file(self, fname, flag):
        return open(fname, flag)

helpString = """Usage: sprint operation [param]. Examples:
    sprint new
    sprint delete [1]
    sprint check 1"""
def sprint_main():
    import sys
    def do_check(op='run'):
        if op == 'check_param': 
            if len(sys.argv)>2: return sys.argv[2] 
            return 'Param_Error'
        else: sprint.check()
        
    def do_initialize(op='run'):
        if op == 'check_param':
            if len(sys.argv)>2: return sys.argv[2] 
            return 'Param_Error'
        else: sprint.initialize()

    def do_new(op='run'):
        if op == 'check_param':
            if len(sys.argv)>2: return 'Param_Error'
            return sprintDir.get_last_num() + 1
        else: sprint.initialize()
    
    def do_delete(op='run'):
        if op == 'check_param':
            if len(sys.argv)>2: return sys.argv[2] 
            return sprintDir.get_last_num()
        else: sprint.delete()
        
    def print_help():
        print helpString
        
    cmdTable = {'check': do_check, 'initialize': do_initialize, \
                'new': do_new, 'delete': do_delete}
        
    if len(sys.argv) == 1 or sys.argv[1] not in cmdTable.keys():
        return print_help()
    
    sprintNum = cmdTable[sys.argv[1]]('check_param')
    if sprintNum == 'Param_Error': return print_help()
    sprint = sprintDir(sprintNum)
    cmdTable[sys.argv[1]]()

if __name__ == '__main__':
    sprint_main()

#! /usr/bin/env python

import os
from os import path

SprintPrefix="Sprint-"
SprintDocList=["sprint_backlog", "sprint_review"]

def get_last_num():
    '''Return the number of the last sprint in current dir'''
    flist=os.listdir(".")
    msi = 0
    for f in flist:
        if f.rfind(SprintPrefix) == 0:
            if int(f.split('-')[1]) > msi: msi = int(f.split('-')[1])
    return msi

    
def create_folder_if_not_exist(folder):
    '''Create folder in case the folder not exist in cur dir'''
    if path.isdir(folder):
        return
    else:
        os.mkdir(folder)

def rmsubsys(folder='.'):
    '''remove a directory
    
    It will work even the folder not empty
    '''
    os.chdir(folder)
    for f in os.listdir('.'):
        if os.path.isdir(f): rmsubsys(f)
        else: os.remove(f)
    if folder == '.': folder=os.path.basename(os.getcwd())
    os.chdir('..')
    os.rmdir(folder)

    
class status:
    available_status=['new', 'ongoing', 'done', 'undefined']
    def __init__(self, st='undefined'):
        self.val='undefined'
        self.update(st)
        
    def update(self, st):
        if st in self.available_status: self.val = st
        
    def show(self):
        return self.val
    
class sprint:
    def __init__(self, st='undefined'):
        self.status = status(st)

    def state(self, newstate=''):
        if newstate == '': return self.status.show()
        else: self.status.update(newstate)    
        

class sprintDoc(sprint):
    '''Define the structure of the sprint documents
    
    sprint documents include sprint_backlog and sprint_review
    '''
    def __init__(self, name="", itemkeys=[]):
        sprint.__init__(self)
        self.name = name
        self.keys = []
        self.items = {'others': []}
        self.init_items(itemkeys)
        
    def init_items(self, itemkeys): 
        self.keys = itemkeys
        for key in itemkeys: self.items[key] = []

    def check(self):
        '''To check the integrity of the document'''
        if self.read() == 0: 
            for key in self.keys:
                print "content check for " + key + " is " + str(self.__content_error(key))
                if self.__content_error(key): self.state('undefined')
        else: 
            self.write()
            self.state('new')
        return self.state()

    def read(self):
        '''read the items out'''
        try:
            f = open(self.name, 'r+')
        except IOError:
            return -1
        for key in self.items.keys(): self.items[key] = []
        cur_key = 'others'
        for line in f:
            for key in self.keys: 
                if line == key + ":\n": 
                    cur_key = key
                    print "find key: " + key
                else: self.items[cur_key].append(line)
        f.close()
        return 0
    
    def write(self):
        '''write the items back'''
        f = open(self.name, 'w+')
        for key in self.keys: 
            f.write(key + ':\n')
            print "content check for " + key + " is " + str(self.__content_error(key))
            if self.__content_error(key): self.items[key].append('')
            f.writelines(self.items[key])
        f.close()

    def __content_error(self, key):
        return (len(self.items[key]) == 0)

class sprintBacklog(sprintDoc):
    def __init__(self):
        sprintDoc.__init__(self, "sprint_backlog", ["Commited Items", "Try Items"])


class sprintReview(sprintDoc):
    def __init__(self):
        sprintDoc.__init__(self, "sprint_review", ["Achievements", "Not done items"])

SprintObjDic={"sprint_backlog":sprintBacklog(), "sprint_review":sprintReview()}

class sprintDir(sprint):
    SprintDocList=["sprint_backlog", "sprint_review"]
    def __init__(self, n):
        sprint.__init__(self)
        self.name = SprintPrefix + str(n)
        self.docs = []
        for doc in self.SprintDocList: self.docs.append(SprintObjDic[doc])
        
    def check(self):
        os.chdir(self.name)
        firstState=self.docs[0].check()
        self.state(firstState)
        for doc in self.docs: 
            status = doc.check()
            if status != firstState:
                if status != 'undefined' and firstState != 'undefined':
                    self.state('ongoing')
                else: 
                    self.state('undefined')
                    break
        print self.name + " status is: " + self.state()
        os.chdir('..')
        
    def destroy(self):
        if self.check() == 'new': rmsubsys(self.name)

    def initialize(self):
        if path.isdir(self.name): rmsubsys(self.name)
        os.mkdir(self.name)
        self.check()
         
class sprintOp:
    '''sprint folder operation

    It used to automatic add new sprint, check integrity of 
    the existing sprint folder.
    '''
    def __init__(self, num):
        self.num = num
        self.sprintDir=sprintDir(0)
        self.docs = []
        for doc in SprintDocList: self.docs.append(SprintObjDic[doc])
        self.name = SprintPrefix + '0'

    def locate_num(self, n):
        self.num = n
        self.name = SprintPrefix+str(n)
        
    def check(self):
        if self.num == 0:
            print "not initialized yet"
            return
        create_folder_if_not_exist(self.name)

        os.chdir(self.name)
        for doc in self.docs: doc.check()
        os.chdir("..")
        
    def new(self):
        self.locate_num(get_last_num() + 1)
        self.check()
        
    def delete(self, n):
        self.locate_num(n)
        rmsubsys(self.name)


if __name__=="__main__":
    sprintOp=sprintOp(0)
    sprintOp.new()


#! /usr/bin/env python

import os
from os import system

SprintPrefix="Sprint-"

def get_last_num():
    '''Return the number of the last sprint in current dir'''
    cmd="ls "+SprintPrefix+"*"
    system(cmd)
    pass
    return 4

    
def create_folder_if_not_exist(folder):
    '''Create folder in case the folder not exist in cur dir'''
    cmd = "mkdir " + folder
    system(cmd)

def create_file_if_not_exist(file):
    '''Create file in case te file not exist in cur dir'''
    print file
    pass

def del_folder(folder):
    cmd = "rm -rf " + folder
    system(cmd)
    
class sprintOp:
    '''sprint folder operation

    It used to automatic add new sprint, check integraty of 
    the existing sprint folder.'''
    def __init__(self):
        self.num = 0
        self.files = ["sprint_backlog", "sprint_review"]
        self.name = SprintPrefix + '0'

    def locate_num(self, n):
        self.num = n
        self.name = SprintPrefix+str(n)
        
    def check_integrate(self):
        if self.num==0 :
            print "not initialized yet"
            return
        create_folder_if_not_exist(self.name)
        for file in self.files: create_file_if_not_exist(file)
        
    def create_new_sprint(self):
        self.locate_num(get_last_num())
        self.check_integrate()
        
    def del_sprint(self, n):
        self.locate_num(n)
        del_folder(self.name)

if __name__=="__main__":
    op=sprintOp()
    op.create_new_sprint()


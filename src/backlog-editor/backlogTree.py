#! /usr/bin/env python

#   Copyright 2012 Chen Gang(fouryusteel@gmail.com)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

def my_open(path, flag='r'):
    return open(path, flag)

def my_close(f):
    return f.close()

class backlogTree:
    defaultAttr = {'priority': 1}
    def __init__(self, content='', subTree=None, attribute=None):
        self._content = content
        self._attribute = attribute
        if not attribute: self._attribute = backlogTree.defaultAttr
        self._subTree = subTree
        if not subTree: self._subTree = []
        self.indent = 0
        
    def _create_sub_node(self, item):
        itemCore = item.strip()
        item = item.replace('\t', ' '*4)
        btNode = backlogTree(itemCore, [], self._attribute)
        btNode.indent = item.rfind(itemCore)
        curNode = self
        while curNode._subTree and btNode.indent > curNode._subTree[-1].indent:
            curNode = curNode._subTree[-1]
        curNode._subTree.append(btNode)

    def _create_sub_tree_from_file(self, f):
        for item in f:
            if item.isspace(): continue
            self._create_sub_node(item)
        
    def init_from_file(self, fileName):
        f = my_open(fileName)
        if not self._content: self._content = fileName
        self._create_sub_tree_from_file(f)
        my_close(f)
            
    def __eq__(self, other):
        if self._content != other._content: return False
        if self._attribute != other._attribute: return False
        if self._subTree != other._subTree: return False
        return True
    
#    def __ne__(self, other):
#        return not self.__eq__(other)
    
    #for checking test result convinient
    def __to_str(self, indent):
        indentStr = ' '*indent
        repStr = indentStr + repr(self._content)+'\n'
        repStr += indentStr + repr(self._attribute) + '\n'
        repStr += indentStr + '[\n'
        for subTree in self._subTree:
            repStr += subTree.__to_str(indent+4) 
        repStr += indentStr + ']\n' 
        return repStr 
        
    def __repr__(self):
        return self.__to_str(0)

def my_open(path, flag='r'):
    return open(path, flag)

def my_close(f):
    return f.close()

class backlogTree:
    defaultAttr = {'priority': 1}
    def __init__(self, content='', attribute=None, subTree=None):
        self._content = content
        self._attribute = attribute
        if not attribute: self._attribute = backlogTree.defaultAttr
        self._subTree = subTree
        if not subTree: self._subTree = []
        
    def init_from_file(self, fileName):
        f=my_open(fileName)
        if not self._content: self._content = fileName
        for item in f:
            item = item.strip()
            self._subTree.append(backlogTree(item, self._attribute))
            
    def __eq__(self, other):
        if self._content != other._content: return False
        if self._attribute != other._attribute: return False
        if self._subTree != other._subTree: return False
        return True
    
#    def __ne__(self, other):
#        return not self.__eq__(other)
    
    #for checking test result convinient
    def __repr__(self):
        repStr = repr(self._content)+'\n'
        repStr += repr(self._attribute) + '\n'
        repStr += '[\n'
        for subTree in self._subTree:
            repStr += '    ' + repr(subTree) + ',\n'
        repStr += ']\n'  
        return repStr

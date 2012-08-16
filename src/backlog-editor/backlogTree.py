def my_open(path, flag):
    return open(path, flag)

class backlogTree:
    defaultAttr = {'priority': 1}
    def __init__(self, content='', subTree=[], attribute={}):
        self._content = content
        self._subTree = subTree
        self._attribute = attribute
        if not attribute: self._attribute = backlogTree.defaultAttr
        
    def init_from_file(self, fileName):
        f=my_open(fileName)
        if not self._content: self._content = fileName
        for item in f:
            item = item.strip()
            self._subTree.append(backlogTree(item, [], self._attribute))
            
    def __eq__(self, other):
        if self._content != other._content: return False
        if self._attribute != other._attribute: return False
        if self._subTree != other._subTree: return False
        return True
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
        
    def _create_sub_node(self, item):
        itemCore = item.strip()
        btNode = backlogTree(itemCore, self._attribute)
        if ' ' == item[0] or '\t' == item[0]: 
            self._subTree[-1]._subTree.append(btNode)
        else: self._subTree.append(btNode)

    def _create_sub_tree_from_file(self, f):
        for item in f:
            if item.isspace(): continue
            self._create_sub_node(item)
        
    def init_from_file(self, fileName):
        f=my_open(fileName)
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

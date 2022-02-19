class Node:
    def __init__(self, type, value, children=None):
        self.type = type
        self.value = value
        if children:
            self.children = children
        else:
            self.children = []

     # __repr__ is used to print the tree
    def __repr__(self, depth=1):
        return_string = [str(self.value)]
        for child in self.children:
            return_string.extend(["\n", "  " * (depth+1), child.__repr__(depth+1)])
        return "".join(return_string)

#======== Map function =======
def mapTree(node, f):
    newType = node.type
    newValue = f(node.value)
    newChildren = []
    for child in node.children:
        newChildren.append(mapTree(child, f))
    
    return Node(newType, newValue, newChildren)
        

# t = Node('BinExpress', '+', [Node('NUMBER', 1), Node('NUMBER', 2)])
# print(t)
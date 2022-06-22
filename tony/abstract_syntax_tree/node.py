import re

class Node:
    def __init__(self, type, value, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []


    def __str__(self, depth=1):
        return_string = [re.sub('\n', lambda _: '\\n', str(self.value))]
        for child in self.children:
            return_string.extend(["\n", "  " * (depth+1), child.__str__(depth+1)])
        return "".join(return_string)

#======== Map function =======
def mapTree(node, f):
    newType = node.type
    newValue = f(node.value)
    newChildren = []
    for child in node.children:
        newChildren.append(mapTree(child, f))

    return Node(newType, newValue, newChildren)

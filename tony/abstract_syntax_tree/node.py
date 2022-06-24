import re
from enum import Enum

class Type(Enum):
   Int  = 1
   Char = 2
   Bool = 3
   Void = 4
   Nil  = 5
   Function = 6 # TODO: Issue #1

class Node:
    def __init__(self, type, value, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []

    def sem(self, symbol_table):
        '''
        Semantic Analysis

        1) Checks that all children are semantically correct
        2) Makes the necessary changes to the symbol table
        3) Returns its type
        '''
        pass

    def __str__(self, depth=1):
        return_string = [re.sub('\n', lambda _: '\\n', str(self.value))]
        for child in self.children:
            return_string.extend(["\n", "  " * (depth+1), child.__str__(depth+1)])
        return "".join(return_string)



class Program(Node):
    def __init__(self, symbol_table, funcdef):
        self.symbol_table = symbol_table
        self.main = funcdef

    def sem(self):
        '''
        1) Recursively checks that the semantics of
        the function definition are correct

        2) TODO: Checks that this function is called main
        '''

        symbol_table.openScope()
        return self.main.sem(symbol_table)


#======== Map function =======
def mapTree(node, f):
    newType = node.type
    newValue = f(node.value)
    newChildren = []
    for child in node.children:
        newChildren.append(mapTree(child, f))

    return Node(newType, newValue, newChildren)

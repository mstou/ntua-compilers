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

    def pprint(self, indent=0):
        return indentation(indent) +\
               f'Instance of {self.__class__.__name__}'

    def __str__(self):
        return self.pprint()


class Program(Node):
    def __init__(self, symbol_table, funcdef):
        self.symbol_table = symbol_table
        self.main = funcdef

    def sem(self):
        '''
            1) Opens the global scope
            2) Checks that the program consists of one function with no parameters
            3) Calls the sem() of the function
        '''

        symbol_table.openScope()

        if self.main.header.params != []:
            errormsg = f'The program should consist of a function with no parameters'
            raise Exception(errormsg)

        return self.main.sem(symbol_table)

    def pprint(self, indent=0):
        s = indentation(indent) + 'Program:\n'
        s += self.main.pprint(indent+2)

        return s

    def __str__(self):
        return self.pprint()


def indentation(indent):
    if indent == 0:
        return ''

    s = ' ' * (indent-2)
    s += '|-- '

    return s
#======== Map function =======
def mapTree(node, f):
    newType = node.type
    newValue = f(node.value)
    newChildren = []
    for child in node.children:
        newChildren.append(mapTree(child, f))

    return Node(newType, newValue, newChildren)

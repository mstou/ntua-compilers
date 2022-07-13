from .data_types import BaseType
from .symbol_table import SymbolTable
from llvmlite import ir, binding

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

    def codegen(self, module, builder, symbol_table):
        '''
            LLVM Code generation

            Adds the necessary instructions to the IR Builder
            and returns an LLVM Value (where applicable)
        '''
        pass

    def pprint(self, indent=0):
        return indentation(indent) +\
               f'Instance of {self.__class__.__name__}'

    def __str__(self):
        return self.pprint()


class Program(Node):
    def __init__(self, funcdef):
        self.main = funcdef
        self.symbol_table = None # will be initialized when sem is called
        self.module  = None
        self.binding = None
        self.builder = None
        self.c_symbol_table = SymbolTable()

    def codegen_init():
        ''' Initializes  llvm '''
        self.binding = binding
        self.binding.initialize()
        self.binding.initialize_native_target()
        self.binding.initialize_native_asmprinter()

        # Declare builder
        self.builder = ir.IRBuilder(block)

    def codegen(self):
        self.codegen_init()
        pass

    def sem(self, symbol_table):
        '''
            1) Opens the global scope
            2) Checks that the program consists of one function with no parameters
            3) Checks that the program consists of a void function
            4) Calls the sem() of the function
        '''
        self.symbol_table = symbol_table
        symbol_table.openScope()

        if self.main.header.params != []:
            errormsg = f'The program should consist of a function with no parameters'
            raise Exception(errormsg)

        self.main.sem(symbol_table)

        entry = symbol_table.lookup(self.main.header.function_name)

        if entry.return_type != BaseType.Void:
            errormsg = f'The program should consist of a function with no return type'
            raise Exception(errormsg)


        return True

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

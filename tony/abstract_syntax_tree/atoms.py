import re
from .node import Node, indentation
from .data_types import *

escape_newline = lambda x: re.sub('\n', lambda _: '\\n', str(x))

class Atom(Node):
    ''' Generic class for atoms '''
    pass

class VarAtom(Atom):
    def __init__(self, name):
        self.name = name

    def sem(self, symbol_table):
        ''' Returns the type of the variable corresponding to the name
            if it exists in some scope, otherwise it raises an Exception.
        '''
        t = symbol_table.lookup(self.name)

        if t != None:
            return t.type

        raise Exception(f'Undefined variable {self.name}.')

    def codegen(self, module, builder, symbol_table):
        '''
            We know that the atom exists from the semantic analysis.
            We look it up in the symbol table and return its llvm value
        '''
        return symbol_table.lookup(self.name).cvalue
        
    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.name}'

    def __str__(self):
        return self.pprint()

class StringAtom(Atom):
    def __init__(self, value):
        self.value = value + '\0'

    def sem(self, symbol_table):
        return Array(BaseType.Char)

    def codegen(self, module, builder, symbol_table):
        '''
            1) Registers a new global variable of type LLVM_Type.Char *
            2) Allocates space and writes the given string
            3) Returns the cvalue of the ptr
        '''
        length = len(self.value)
        llvm_value = ir.Constant(ir.ArrayType(LLVM_Type.Char, length),
                                 bytearray(self.value.encode("utf-8"))
                                )
        ptr = self.builder.alloca(llvm_value.type)
        builder.store(llvm_value, ptr)

        return ptr

    def pprint(self, indent=0):
        return f'{indentation(indent)}{escape_newline(self.value)}'

    def __str__(self):
        return self.pprint()

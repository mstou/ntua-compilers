from .node         import Node, indentation
from .data_types   import *
from .llvm_types   import LLVM_Types

import re
from llvmlite import ir

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
        self.value = value[1:-1] + '\0' # get rid of the "" and add terminating character

    def sem(self, symbol_table):
        return Array(BaseType.Char)

    def codegen(self, module, builder, symbol_table):
        '''
            1) Registers a new global variable of type LLVM_Type.Char *
            2) Allocates space and writes the given string
            3) Returns the cvalue of the ptr
        '''
        length   = len(self.value)
        str_type = ir.ArrayType(LLVM_Types.Char, length)
        llvm_value = ir.GlobalVariable(module, str_type,
                                       f'str_literal_{symbol_table.get_id()}'
                                       )
        llvm_value.initializer = ir.Constant(str_type, bytearray(self.value.encode("utf-8")))
        char_ptr = LLVM_Types.Char.as_pointer()
        str_ptr  = builder.bitcast(llvm_value, char_ptr)
        return str_ptr

    def pprint(self, indent=0):
        return f'{indentation(indent)}{escape_newline(self.value)}'

    def __str__(self):
        return self.pprint()

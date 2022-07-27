from .node         import Node, indentation
from .symbol_table import Variable
from .llvm_types   import BaseType_to_LLVM
from .data_types   import List

from llvmlite import ir

class VariableDefinition(Node):
    def __init__(self, type, names):
        self.type = type
        self.names = names
        self.llvm_type = None

    def sem(self, symbol_table):
        '''
            1) Checks that the name does not already exist in the scope

            2) Inserts the variable to the current scope
        '''
        type = self.type.sem(symbol_table)
        self.llvm_type = BaseType_to_LLVM(type, var_definition=True)

        for name in self.names:
            if symbol_table.lookup_current_scope(name) != None:
                errormsg = f'Syntax Error. Variable {name} is already defined.'
                raise Exception(errormsg)

            symbol_table.insert(name, Variable(name,type))

        return type

    def codegen(self, module, builder, symbol_table):
        '''
            We know from sem() that the name does not exist.
            We add the variable in the symbol table along with its LLVM value
        '''
        t = self.llvm_type

        cvalues = []
        for name in self.names:
            cvalue = builder.alloca(t)
            builder.store(ir.Constant(t, None), cvalue) # initializer
            cvalues.append(cvalue)
            symbol_table.insert(name, Variable(name, t, cvalue))

        return cvalues

    def pprint(self, indent=0):
        return indentation(indent) + f'{self.type} ' +\
               ', '.join(self.names)

    def __str__(self):
        return self.pprint()



class NameList(Node):
    def __init__(self, name, names):
        self.name  = name
        self.names = names

    def getNames(self):
        if self.name == None:
            return []

        return [self.name] + self.names.getNames()

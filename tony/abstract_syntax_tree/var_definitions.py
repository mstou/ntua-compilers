from .node         import Node, indentation
from .symbol_table import Variable
from .llvm_types   import BaseType_to_LLVM
from llvmlite import ir

class VariableDefinition(Node):
    def __init__(self, type, names):
        self.type = type
        self.names = names

    def sem(self, symbol_table):
        '''
            1) Checks that the name does not already exist in the scope

            2) Inserts the variable to the current scope
        '''
        type = self.type.sem(symbol_table)

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
        t = BaseType_to_LLVM(self.type)
        cvalues = []
        for names in self.names:
            cvalue = ir.GlobalVariable(module, t, f'{name}_{symbol_table.get_id()}')
            cvalues.append(cvalue)
            symbol_table.insert(Variable(name, self.type, cvalue))

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

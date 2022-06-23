from .node import Node

class VariableDefinition(Node):
    def __init__(self, type, names):
        self.type = type
        self.names = names
        

    def sem(self, symbol_table):
        '''
        1) Checks that the name does not already exist in the scope
        2) Add the variable to the current scope
        '''
        for name in self.names:
            if symbol_table.lookup_current_scope(name) != None:
                errormsg = f'Syntax Error. Variable {name} is already defined.'
                raise Exception(errormsg)

            symbol_table.insert(name, self.type)

        return True


class NameList(Node):
    def __init__(self, name, names):
        self.name  = name
        self.names = names

    def getNames(self):
        if self.name == None:
            return []

        return [self.name] + self.names.getNames()

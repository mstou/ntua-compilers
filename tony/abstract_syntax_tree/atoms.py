import re
from .node import Node, indentation

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
            return t

        raise Exception(f'Undefined variable {self.name}.')


    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.name}'

    def __str__(self):
        return self.pprint()

class StringAtom(Atom):
    def __init__(self, value):
        self.value = value

    def sem(self, symbol_table):
        return Array(BaseType.Char)

    def pprint(self, indent=0):
        return f'{indentation(indent)}{escape_newline(self.value)}'

    def __str__(self):
        return self.pprint()

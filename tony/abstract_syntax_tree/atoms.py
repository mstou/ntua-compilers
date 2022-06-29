import re
from .node import Node, indentation

escape_newline = lambda x: re.sub('\n', lambda _: '\\n', str(x))

class Atom(Node):
    ''' Generic class for atoms '''
    pass

class VarAtom(Atom):
    def __init__(self, name):
        self.name = name

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.name}'

    def __str__(self):
        return self.pprint()

class StringAtom(Atom):
    def __init__(self, value):
        self.value = value

    def pprint(self, indent=0):
        return f'{indentation(indent)}{escape_newline(self.value)}'

    def __str__(self):
        return self.pprint()

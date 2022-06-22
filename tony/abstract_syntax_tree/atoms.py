from .node import Node

class Atom(Node):
    ''' Generic class from atoms '''
    pass

class VarAtom(Atom):
    def __init__(self, id, name=None):
        self.id   = id
        self.name = name

class StringAtom(Atom):
    def __init__(self, value):
        self.value = value

from .node import Node

class Type(Node):
    ''' General Class for Data Types '''
    pass

class Array(Type):
    def __init__(self, type):
        self.type = type

class List(Type):
    def __init__(self, type):
        self.type = type

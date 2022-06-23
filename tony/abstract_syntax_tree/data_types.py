from .node import Node

class TypeNode(Node):
    ''' General Class for Data Types '''
    pass

class Array(TypeNode):
    def __init__(self, type):
        self.type = type

class List(TypeNode):
    def __init__(self, type):
        self.type = type

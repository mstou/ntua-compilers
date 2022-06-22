from .node import Node

class Type(Node):
    ''' General Class for Data Types '''
    pass

class Int(Type):
    def __init__(self, data):
        self.data = data

class Bool(Type):
    def __init__(self, data):
        self.data = data

class Char(Type):
    def __init__(self, data):
        self.data = data

class Array(Type):
    def __init__(self, type):
        self.type = type

class List(Type):
    def __init__(self, type):
        self.type = type

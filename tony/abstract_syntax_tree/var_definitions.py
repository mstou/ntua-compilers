from .node import Node

class VariableDefinition(Node):
    def __init__(self, type, name, vars):
        self.type = type
        self.name = name
        self.vars = vars

class Name(Node):
    def __init__(self, name):
        self.name = name

class NameList(Node):
    def __init__(self, name, names):
        self.name  = name
        self.names = names

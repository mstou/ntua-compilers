from .node import Node
from enum import Enum

class Type:
    ''' Abstract class for Tony Types '''
    pass

class BaseType(Type, Enum):
   Int  = 'int'
   Char = 'char'
   Bool = 'bool'
   Void = 'void'
   Nil  = 'nil' # empty list of any type

   def __eq__(self, other):
       if isinstance(other, self.__class__):
          return self.value == other.value

       return False

   def __str__(self):
       return self.value

class CompositeType(Type):
    ''' Abstract class for Composite Types '''
    pass


class List(CompositeType):
    def __init__(self, t):
        self.t = t # subtype

    def __eq__(self, other):
        if isinstance(other, BaseType.__class__):
            return other == BaseType.Nil

        if isinstance(other, self.__class__):
            return self.t == other.t

        return False

    def __str__(self):
        return f'List of {self.t}'


class Array(CompositeType):
    def __init__(self, t):
        self.t = t # subtype

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.t == other.t

        return False

    def __str__(self):
        return f'Array of {self.t}'


class Function(CompositeType):
    def __init__(self, return_type, params):
        self.return_type = return_type
        self.params      = params

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.return_type == other.return_type and\
                   self.params == other.params

    def __str__(self):
        return f'Function ({", ".join(self.params)}) -> {self.return_type}'

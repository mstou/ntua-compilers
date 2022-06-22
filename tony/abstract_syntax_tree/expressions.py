from .node import Node

class Expression(Node):
    ''' Generic class for expressions '''

    def eval(self):
        ''' Returns the value of the expression '''
        pass

class ParenthesisExpr(Expression):
    def __init__(self, expr):
        self.expr = expr

class BinaryOperator(Expression):
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right

class BinaryComparison(Expression):
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right

class Not(Expression):
    def __init__(self, expr):
        self.expr  = expr

class BinaryBoolean(Expression):
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right

class Int(Expression):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data

class Bool(Expression):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data

class Char(Expression):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data

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

class IntValue(Expression):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data

class BooleanValue(Expression):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data

class CharValue(Expression):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data

class AtomArray(Expression):
    def __init__(self, atom, expr):
        self.atom = atom
        self.expr = expr

class UniArithmeticPLUS(Expression):
    def __init__(self, expr):
        self.expr = expr

class UniArithmeticMINUS(Expression):
    def __init__(self, expr):
        self.expr = expr

class NewArray(Expression):
    def __init__(self, type, expr):
        self.type = type
        self.expr = expr

class isEmptyList(Expression):
    def __init__(self, expr):
        self.expr = expr

class ListOperator(Expression):
    def __init__(self, left, right):
        self.head = left
        self.tail = right

class TailOperator(Expression):
    def __init__(self, expr):
        self.expr = expr

class HeadOperator(Expression):
    def __init__(self, expr):
        self.expr = expr

class CommaExpr(Expression):
    def __init__(self, expr, comma_expr):
        self.expr = expr
        self.comma_expr = comma_expr

    def getExpressions(self):
        return [] if self.expr == None\
        else [self.expr] + self.comma_expr.getExpressions()

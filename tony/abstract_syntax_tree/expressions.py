from .node import Node

class Expression(Node):
    ''' Generic class for expressions '''

    def eval(self):
        ''' Returns the value of the expression '''
        pass

    def sem(self, symbol_table):
        ''' Checks that the semantics are correct and
            returns the type of the expression '''
        pass

class ParenthesisExpr(Expression):
    def __init__(self, expr):
        self.expr = expr

    def sem(self, symbol_table):
        return self.expr.sem()

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

    def sem(self, symbol_table):
        t = self.expr.sem()

        if t != Type.Bool:
            error_msg = f'Expected the operand of not\
            to be of type Bool but {t} was given.'

            raise Exception(error_msg)

        return Type.Bool

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

    def sem(self, symbol_table):
        return Type.Int

class BooleanValue(Expression):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data

    def sem(self, symbol_table):
        return Type.Bool

class CharValue(Expression):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data

    def sem(self, symbol_table):
        return Type.Char

class AtomArray(Expression):
    def __init__(self, atom, expr):
        self.atom = atom
        self.expr = expr

class UniArithmeticPLUS(Expression):
    def __init__(self, expr):
        self.expr = expr

    def sem(self, symbol_table):
        t = self.expr.sem()

        if t != Type.Int:
            error_msg = f'Can not use unary "+"\
            with type {t}'

            raise Exception(error_msg)

        return t

class UniArithmeticMINUS(Expression):
    def __init__(self, expr):
        self.expr = expr


    def sem(self, symbol_table):
        t = self.expr.sem()

        if t != Type.Int:
            error_msg = f'Can not use unary "-"\
            with type {t}'

            raise Exception(error_msg)

        return t

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

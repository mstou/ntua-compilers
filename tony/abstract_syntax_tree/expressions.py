from .node import Node, indentation

class Expression(Node):
    ''' Generic class for expressions '''

    def eval(self):
        ''' Returns the value of the expression '''
        pass

    def sem(self, symbol_table):
        ''' Checks that the semantics are correct and
            returns the type of the expression '''
        pass

    def pprint(self, indent=0):
        ''' Pretty-printing of the Node with custom indentation '''
        pass

class ParenthesisExpr(Expression):
    def __init__(self, expr):
        self.expr = expr

    def sem(self, symbol_table):
        return self.expr.sem()

    def pprint(self, indent = 0):
        return f'{indentation(indent)}({self.expr})'

    def __str__(self, ):
        return self.pprint()

class BinaryOperator(Expression):
    ''' Node for binary arithmetic expressions.
        Operators are: +, -, *, /, %
    '''
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right

    def sem(self, symbol_table):
        '''
            1) Calls the sem() function of the left and right expressions
               to get their types.

            2) Checks that the types are compatible and it raises an
               Exception if they are not.

            3) Returns the type of the expression.
        '''

        t1 = self.left.sem(symbol_table)
        t2 = self.right.sem(symbol_table)

        if t1 != BaseType.Int or t2 != BaseType.Int:
            errormsg = f'Invalid operants. Operator {self.op}\
                         can not be used with {t1} and {t2}.'

            raise Exception(errormsg)

        return BaseType.Int

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.op}\n' +\
               self.left.pprint(indent+2)+'\n'+\
               self.right.pprint(indent+2)

    def __str__(self):
        return self.pprint()

class BinaryComparison(Expression):
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.op}\n' +\
               self.left.pprint(indent+2)+'\n'+\
               self.right.pprint(indent+2)

    def __str__(self):
        return self.pprint()

class Not(Expression):
    def __init__(self, expr):
        self.expr  = expr

    def sem(self, symbol_table):
        t = self.expr.sem()

        if t != BaseType.Bool:
            error_msg = f'Expected the operand of not\
            to be of type Bool but {t} was given.'
            raise Exception(error_msg)

        return BaseType.Bool

    def pprint(self, indent=0):
        return f'{indentation(indent)}not\n'+\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()

class BinaryBoolean(Expression):
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.op}\n' +\
               self.left.pprint(indent+2)+'\n'+\
               self.right.pprint(indent+2)

    def __str__(self):
        return self.pprint()

class IntValue(Expression):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data

    def sem(self, symbol_table):
        return BaseType.Int

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.data}'

    def __str__(self):
        return self.pprint()

class BooleanValue(Expression):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data

    def sem(self, symbol_table):
        return BaseType.Bool

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.data}'

    def __str__(self):
        return self.pprint()

class CharValue(Expression):
    def __init__(self, data):
        self.data = data

    def eval(self):
        return self.data

    def sem(self, symbol_table):
        return BaseType.Char

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.data}'

    def __str__(self):
        return self.pprint()

class AtomArray(Expression):
    def __init__(self, atom, expr):
        self.atom = atom
        self.expr = expr

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.atom}[ . ]\n'+\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()

class UniArithmeticPLUS(Expression):
    def __init__(self, expr):
        self.expr = expr

    def sem(self, symbol_table):
        t = self.expr.sem()

        if t != BaseType.Int:
            error_msg = f'Can not use unary "+"\
            with type {t}'

            raise Exception(error_msg)

        return t

    def pprint(self, indent=0):
        return f'{indentation(indent)}unary (+)\n' +\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()

class UniArithmeticMINUS(Expression):
    def __init__(self, expr):
        self.expr = expr

    def sem(self, symbol_table):
        t = self.expr.sem()

        if t != BaseType.Int:
            error_msg = f'Can not use unary "-"\
            with type {t}'

            raise Exception(error_msg)

        return t

    def pprint(self, indent=0):
        return f'{indentation(indent)}unary (-)\n' +\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()


class NewArray(Expression):
    def __init__(self, type, expr):
        self.type = type
        self.expr = expr

    def pprint(self, indent=0):
        return f'{indentation(indent)}new array {self.type} of length\n'+\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()


class isEmptyList(Expression):
    def __init__(self, expr):
        self.expr = expr

    def pprint(self, indent=0):
        return f'{indentation(indent)}nil?\n'+\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()

class ListOperator(Expression):
    def __init__(self, left, right):
        self.head = left
        self.tail = right

    def pprint(self, indent=0):
        return f'{indentation(indent)}new list with (head,tail):\n'+\
               self.head.pprint(indent=indent+2)+'\n'+\
               self.tail.pprint(indent=indent+2)

class TailOperator(Expression):
    def __init__(self, expr):
        self.expr = expr

    def pprint(self, indent=0):
        return f'{indentation(indent)}tail of\n'+\
               self.expr.pprint(indent=indent+2)
    def __str__(self):
        return self.pprint()

class HeadOperator(Expression):
    def __init__(self, expr):
        self.expr = expr

    def pprint(self, indent=0):
        return f'{indentation(indent)}head of\n'+\
               self.expr.pprint(indent=indent+2)
    def __str__(self):
        return self.pprint()

class CommaExpr(Expression):
    def __init__(self, expr, comma_expr):
        self.expr = expr
        self.comma_expr = comma_expr

    def getExpressions(self):
        return [] if self.expr == None\
        else [self.expr] + self.comma_expr.getExpressions()

    def pprint(self, indent=0):
        s = f'{indentation(indent)}Comma Separated Expressions:\n'

        expressions = self.getExpressions()
        n = len(expressions)

        for i,e in enumerate(expressions):
            s += e.pprint(indent=indent+2)
            if i != n-1:
                s += '\n'

        return s

    def __str__(self):
        return self.pprint()

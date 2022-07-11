from .node import Node, indentation
from .data_types import *
from llvmlite import ir
from .llvm_types import LLVM_Types

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
        return self.expr.sem(symbol_table)

    def codegen(self, module, builder):
        return self.expr.codegen(module, builder)

    def pprint(self, indent = 0):
        return indentation(indent) + 'Parenthesis\n' +\
               self.expr.pprint(indentation+2) + '\n'

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
            errormsg = f'Invalid operants. Operator {self.op}' +\
                       f'can not be used with {t1} and {t2}.'

            raise Exception(errormsg)

        return BaseType.Int

    def codegen(self, module, builder):
        lhs = self.left.codegen(module, builder)
        rhs = self.right.codegen(module, builder)

        if self.op == '+':
            return builder.add(lhs, rhs, name='addtmp')
        elif self.op == '-':
            return builder.sub(lhs, rhs, name='subtmp')
        elif self.op == '*':
            return builder.mul(lhs, rhs, name='multmp')
        elif self.op == '/':
            return builder.sdiv(lhs, rhs, name='divtmp')
        elif self.op == '%':
            return builder.srem(lhs, rhs, name='divtmp')
        else:
            return None

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.op}\n' +\
               self.left.pprint(indent+2)+'\n'+\
               self.right.pprint(indent+2)

    def __str__(self):
        return self.pprint()

class BinaryComparison(Expression):
    ''' Node for binary comparisons.
        Operators are: =, <>, <, >, <=, >=
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
               Exception if they are not. For = and <> the operants
               must be of the same BaseType. For >, <, <=, >= the operants
               must be BaseType.Int or BaseType.Char

            3) Returns the type of the expression.
        '''

        t1 = self.left.sem(symbol_table)
        t2 = self.right.sem(symbol_table)

        if t1 != t2 or t1 not in [BaseType.Int, BaseType.Bool, BaseType.Char]:
            errormsg = f'Invalid operants. Operator {self.op}' +\
                       f'can not be used with {t1} and {t2}.'
            raise Exception(errormsg)

        if self.op in ['>', '<', '>=', '<='] and t1 == BaseType.Bool:
            errormsg = f'Operator {self.op} is not supported for Booleans.'

            raise Exception(errormsg)

        return BaseType.Bool

    def codegen(self, module, builder):
        lhs = self.left.codegen(module, builder)
        rhs = self.right.codegen(module, builder)

        character_map = {
        '=': '==', '<>': '!=',
        '<': '<', '>': '>', '<=': '<=', '>=': '>='
        }

        if self.op in character_map:
            builder.icmp_unsigned(character_map[self.op], lhs, rhs, name=f'comparisontmp{self.op}')
        else:
            return None

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
        t = self.expr.sem(symbol_table)

        if t != BaseType.Bool:
            error_msg = f'Expected the operand of not\
            to be of type Bool but {t} was given.'
            raise Exception(error_msg)

        return BaseType.Bool

    def codegen(self, module, builder):
        expr = self.expr.codegen(module, builder)
        return builder.not_(expr, name = 'nottmp')

    def pprint(self, indent=0):
        return f'{indentation(indent)}not\n'+\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()

class BinaryBoolean(Expression):
    ''' Node for binary logical expressions.
        Operators are: and, or
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

        if t1 != BaseType.Bool or t2 != BaseType.Bool:
            errormsg = f'Invalid operants. Operator {self.op}' +\
                       f'can not be used with {t1} and {t2}.'

            raise Exception(errormsg)

        return BaseType.Bool

    def codegen(self, module, builder):
        lhs = self.left.codegen(module, builder)
        rhs = self.right.codegen(module, builder)

        if self.op == 'and':
            return builder.and_(lhs, rhs, name = 'andtmp')
        elif self.op == 'or':
            return builder.or_(lhs, rhs, name = 'ortmp')
        else:
            return None

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.op}\n' +\
               self.left.pprint(indent+2)+'\n'+\
               self.right.pprint(indent+2)

    def __str__(self):
        return self.pprint()

class ArrayNode(Expression):
    def __init__(self, type):
        self.type = type

    def sem(self, symbol_table):
        return Array(self.type.sem(symbol_table))

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.type}'

    def __str__(self):
        return self.pprint()


class ListNode(Expression):
    def __init__(self, type):
        self.type = type

    def sem(self, symbol_table):
        return List(self.type.sem(symbol_table))

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.type}'

    def __str__(self):
        return self.pprint()

class VoidNode(Expression):
    def __init__(self):
        pass

    def sem(self, symbol_table):
        return BaseType.Void

    def pprint(self, indent=0):
        return f'{indentation(indent)}{BaseType.Void}'

    def __str__(self):
        return self.pprint()

class EmptyListNode(Expression):
    def __init__(self):
        pass

    def sem(self, symbol_table):
        return BaseType.Nil

    def pprint(self, indent=0):
        return f'{indentation(indent)}{BaseType.Void}'

    def __str__(self):
        return self.pprint()

class IntValue(Expression):
    def __init__(self, data):
        self.data = data

    def sem(self, symbol_table):
        return BaseType.Int

    def codegen(self, module, builder):
        return ir.Constant(LLVM_Types.Int, self.data)

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.data}'

    def __str__(self):
        return self.pprint()

class BooleanValue(Expression):
    def __init__(self, data):
        self.data = data

    def sem(self, symbol_table):
        return BaseType.Bool

    def codegen(self, module, builder):
        return ir.Constant(LLVM_Types.Bool, 1 if self.data else 0)

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.data}'

    def __str__(self):
        return self.pprint()

class CharValue(Expression):
    def __init__(self, data):
        self.data = data

    def sem(self, symbol_table):
        return BaseType.Char

    def codegen(self, module, builder):
        return ir.Constant(LLVM_Types.Char, ord(self.data))
        # TODO: do we have to fix escaped characters?

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.data}'

    def __str__(self):
        return self.pprint()

class AtomArray(Expression):
    def __init__(self, atom, expr):
        self.atom = atom
        self.expr = expr

    def sem(self, symbol_table):
        '''
            1) Checks that the name exists and is indeed an array
            2) Checks that the expr has type Int
            3) Returns the type of the expr
        '''
        atom_type = self.atom.sem(symbol_table)

        if not isinstance(atom_type, Array):
            errormsg = f'Type {atom_type} is not subscriptable'
            raise Exception(errormsg)

        expr_type = self.expr.sem(symbol_table)

        if expr_type != BaseType.Int:
            errormsg = 'Indices of arrays can only be of type int'
            raise Exception(errormsg)

        return atom_type.t

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.atom}[ . ]\n'+\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()

class UniArithmeticPLUS(Expression):
    def __init__(self, expr):
        self.expr = expr

    def sem(self, symbol_table):
        t = self.expr.sem(symbol_table)

        if t != BaseType.Int:
            error_msg = f'Can not use unary "+"\
            with type {t}'

            raise Exception(error_msg)

        return t

    def codegen(self, module, builder):
        return self.expr.codegen(module, builder)

    def pprint(self, indent=0):
        return f'{indentation(indent)}unary (+)\n' +\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()

class UniArithmeticMINUS(Expression):
    def __init__(self, expr):
        self.expr = expr

    def sem(self, symbol_table):
        t = self.expr.sem(symbol_table)

        if t != BaseType.Int:
            error_msg = f'Can not use unary "-"\
            with type {t}'

            raise Exception(error_msg)

        return t

    def codegen(self, module, builder):
        expr = self.expr.codegen(module, builder)
        return builder.neg(expr, 'unaryminustmp')

    def pprint(self, indent=0):
        return f'{indentation(indent)}unary (-)\n' +\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()


class NewArray(Expression):
    def __init__(self, type, expr):
        self.type = type
        self.expr = expr

    def sem(self, symbol_table):
        '''
            1) Checks that the expr is of type BaseType.Int
            2) Returns the type of the new array
        '''
        expr_type = self.expr.sem(symbol_table)

        if expr_type != BaseType.Int:
            errormsg = f'The length of an array can only be of type {BaseType.Int}'
            raise Exception(errormsg)

        return Array(self.type.sem(symbol_table))

    def pprint(self, indent=0):
        return f'{indentation(indent)}new array {self.type} of length\n'+\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()


class isEmptyList(Expression):
    def __init__(self, expr):
        self.expr = expr

    def sem(self, symbol_table):
        '''
            Checks that the given expression is a list.
        '''
        expr_type = self.expr.sem(symbol_table)

        if expr_type != BaseType.Nil and not isinstance(expr_type, List):
            errormsg = f'nil? expects a list as a parameter but a {expr_type} was given.'
            raise Exception(errormsg)

        return BaseType.Bool

    def pprint(self, indent=0):
        return f'{indentation(indent)}nil?\n'+\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()

class ListOperator(Expression):
    def __init__(self, left, right):
        self.head = left
        self.tail = right

    def sem(self, symbol_table):
        '''
            1) Find the type of the head and checks that the tail is either an
               empty list or a list of that type.

            2) Returns the type of the list
        '''
        head_type = self.head.sem(symbol_table)
        tail_type = self.tail.sem(symbol_table)

        if tail_type != BaseType.Nil and tail_type != List(head_type):
            errormsg = f'Incompatible types of head and tail. Expected' +\
                       f'{List(head_type)} but got {tail_type} instead.'

            raise Exception(errormsg)

        return List(head_type)

    def pprint(self, indent=0):
        return f'{indentation(indent)}new list with (head,tail):\n'+\
               self.head.pprint(indent=indent+2)+'\n'+\
               self.tail.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()

class TailOperator(Expression):
    def __init__(self, expr):
        self.expr = expr

    def sem(self, symbol_table):
        '''
            1) Checks that the given expression is a list and not BaseType.Nil

            2) Returns the type of the list
        '''

        t = self.expr.sem(symbol_table)

        if not isinstance(t, List):
            errormsg = f'Tail operator can not be used with type {t}.'
            raise Exception(errormsg)

        return t

    def pprint(self, indent=0):
        return f'{indentation(indent)}tail of\n'+\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()

class HeadOperator(Expression):
    def __init__(self, expr):
        self.expr = expr

    def sem(self, symbol_table):
        '''
            1) Checks that the given expression is a list and not BaseType.Nil

            2) Returns the type of the list
        '''

        t = self.expr.sem(symbol_table)

        if not isinstance(t, List):
            errormsg = f'Head operator can not be used with type {t}.'
            raise Exception(errormsg)

        return t.t # list subtype

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

    def sem(self, symbol_table):
        ''' This is not implemented and will never be called.
            The CommaExpr is only used for Function Calls where
            we will call the sem() function of each expression
            separately.
        '''
        pass

    def codegen(self, module, builder):
        ''' This is not implemented and will never be called.
            The CommaExpr is only used for Function Calls where
            we will call the codegen() function of each expression
            separately.
        '''
        pass

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

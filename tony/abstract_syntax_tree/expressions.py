from .node         import Node, indentation
from .data_types   import *
from .llvm_types   import LLVM_Types, BaseType_to_LLVM
from .symbol_table import FunctionParam
from .atoms        import VarAtom

from llvmlite import ir

def should_load_or_store(expression, symbol_table):
    # global variables, arrays, lists and function params that
    # are passed by reference must be loaded before use
    # and stored after assignments

    if isinstance(expression, AtomArray) or isinstance(expression, List):
        return True

    if not isinstance(expression, VarAtom):
        return False

    # the expression is a variable
    var_entry = symbol_table.lookup(expression.name)

    if isinstance(var_entry, FunctionParam):
        return var_entry.reference

    return True


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

    def codegen(self, module, builder, symbol_table):
        return self.expr.codegen(module, builder, symbol_table)

    def pprint(self, indent = 0):
        return indentation(indent) + 'Parenthesis\n' +\
               self.expr.pprint(indent+2) + '\n'

    def __str__(self, ):
        return self.pprint()

class BinaryOperator(Expression):
    ''' Node for binary arithmetic expressions.
        Operators are: +, -, *, /, mod
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

    def codegen(self, module, builder, symbol_table):
        lhs = self.left.codegen(module, builder, symbol_table)
        rhs = self.right.codegen(module, builder, symbol_table)

        if should_load_or_store(self.left, symbol_table):
            lhs = builder.load(lhs)

        if should_load_or_store(self.right, symbol_table):
            rhs = builder.load(rhs)

        if self.op == '+':
            return builder.add(lhs, rhs, name='addtmp')
        elif self.op == '-':
            return builder.sub(lhs, rhs, name='subtmp')
        elif self.op == '*':
            return builder.mul(lhs, rhs, name='multmp')
        elif self.op == '/':
            return builder.sdiv(lhs, rhs, name='divtmp')
        elif self.op == 'mod':
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

    def codegen(self, module, builder, symbol_table):
        lhs = self.left.codegen(module, builder, symbol_table)
        rhs = self.right.codegen(module, builder, symbol_table)

        character_map = {
        '=': '==', '<>': '!=',
        '<': '<', '>': '>', '<=': '<=', '>=': '>='
        }

        if should_load_or_store(self.left, symbol_table):
            lhs = builder.load(lhs)

        if should_load_or_store(self.right, symbol_table):
            rhs = builder.load(rhs)

        if self.op in character_map:
            return builder.icmp_unsigned(character_map[self.op], lhs, rhs, name=f'comparisontmp{self.op}')
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

    def codegen(self, module, builder, symbol_table):
        expr = self.expr.codegen(module, builder, symbol_table)

        if should_load_or_store(self.expr, symbol_table):
            expr = builder.load(expr)

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

    def codegen(self, module, builder, symbol_table):
        lhs = self.left.codegen(module, builder, symbol_table)
        rhs = self.right.codegen(module, builder, symbol_table)

        if should_load_or_store(self.left, symbol_table):
            lhs = builder.load(lhs)

        if should_load_or_store(self.right, symbol_table):
            rhs = builder.load(rhs)

        if self.op == 'and':
            return builder.and_(lhs, rhs, name = 'andtmp')
        elif self.op == 'or':
            return builder.or_(lhs, rhs, name = 'ortmp')
        else:
            return None

        #TODO: implement short circuit evaluation

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
        return f'{indentation(indent)}{BaseType.Nil}'

    def codegen(self, module, builder, symbol_table, type):
        # expects the type of list to construct
        # a nullptr for the correct data_type

        node = BaseType_to_LLVM(type)
        return ir.Constant(node.as_pointer(), None)

    def __str__(self):
        return self.pprint()

class IntValue(Expression):
    def __init__(self, data):
        self.data = data

    def sem(self, symbol_table):
        return BaseType.Int

    def codegen(self, module, builder, symbol_table):
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

    def codegen(self, module, builder, symbol_table):
        return ir.Constant(LLVM_Types.Bool, 1 if self.data=="true" else 0)

    def pprint(self, indent=0):
        return f'{indentation(indent)}{self.data}'

    def __str__(self):
        return self.pprint()

class CharValue(Expression):
    def __init__(self, data):
        self.data = data[1:-1]

    def sem(self, symbol_table):
        return BaseType.Char

    def codegen(self, module, builder, symbol_table):
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
        self.name = atom.name

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

    def codegen(self, module, builder, symbol_table):
        array_ptr = self.atom.codegen(module, builder, symbol_table)

        if should_load_or_store(self.atom, symbol_table):
            array_ptr = builder.load(array_ptr)

        expr_cvalue = self.expr.codegen(module, builder, symbol_table)

        if should_load_or_store(self.expr, symbol_table):
            expr_cvalue = builder.load(expr_cvalue)

        pointer_to_elem = builder.gep(array_ptr, [expr_cvalue])

        return pointer_to_elem

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

    def codegen(self, module, builder, symbol_table):
        return self.expr.codegen(module, builder, symbol_table)

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

    def codegen(self, module, builder, symbol_table):
        expr = self.expr.codegen(module, builder, symbol_table)

        if should_load_or_store(self.expr, symbol_table):
            expr = builder.load(expr)

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

        type = self.type.sem(symbol_table)
        self.llvm_array_type = BaseType_to_LLVM(type)
        return Array(type)

    def codegen(self, module, builder, symbol_table):
        expr_cvalue = self.expr.codegen(module, builder, symbol_table)
        return builder.alloca(self.llvm_array_type, expr_cvalue)

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
        self.list_type = None
        self.tail_type = None

    def sem(self, symbol_table):
        '''
            1) Find the type of the head and checks that the tail is either an
               empty list or a list of that type.

            2) Returns the type of the list
        '''
        head_type = self.head.sem(symbol_table)
        tail_type = self.tail.sem(symbol_table)

        self.list_type = List(head_type)
        self.tail_type = tail_type

        if tail_type != BaseType.Nil and tail_type != List(head_type):
            errormsg = f'Incompatible types of head and tail. Expected ' +\
                       f'{List(head_type)} but got {tail_type} instead.'

            raise Exception(errormsg)

        return List(head_type)

    def codegen(self, module, builder, symbol_table):
        one  = ir.Constant(LLVM_Types.Int, 1)
        zero = ir.Constant(LLVM_Types.Int, 0)

        head_c = self.head.codegen(module, builder, symbol_table)

        if isinstance(self.tail_type, BaseType): # self.tail_type == BaseType.Nil
            tail_c = self.tail.codegen(module, builder, symbol_table, type=self.list_type)
        else:
            tail_c = self.tail.codegen(module, builder, symbol_table)

        if should_load_or_store(self.head, symbol_table):
            head_c = builder.load(head_c)

        if should_load_or_store(self.tail, symbol_table):
            tail_c = builder.load(tail_c)

        list_node = BaseType_to_LLVM(self.list_type)
        new_block = builder.alloca(list_node)

        head_ptr = builder.gep(new_block, [zero, zero])
        tail_ptr = builder.gep(new_block, [zero, one])

        builder.store(head_c, head_ptr, align=1)
        builder.store(tail_c, tail_ptr, align=1)

        return new_block

    def pprint(self, indent=0):
        return f'{indentation(indent)}new list with (head,tail):\n'+\
               self.head.pprint(indent=indent+2)+'\n'+\
               self.tail.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()

class TailOperator(Expression):
    def __init__(self, expr):
        self.expr = expr
        self.expr_type = None

    def sem(self, symbol_table):
        '''
            1) Checks that the given expression is a list and not BaseType.Nil

            2) Returns the type of the list
        '''

        t = self.expr.sem(symbol_table)

        self.expr_type = t

        if not isinstance(t, List):
            errormsg = f'Tail operator can not be used with type {t}.'
            raise Exception(errormsg)

        return t

    def codegen(self, module, builder, symbol_table):
        # self.expr will not be Nil - guaranteed by the semantics check
        # however, it might be an atom that points to an empty list.
        # in that case it will crach during execution
        list_cvalue = self.expr.codegen(module, builder, symbol_table)

        if should_load_or_store(self.expr, symbol_table):
            list_cvalue = builder.load(list_cvalue)

        zero = ir.Constant(LLVM_Types.Int, 0)
        one  = ir.Constant(LLVM_Types.Int, 1)

        ptr_to_head = builder.gep(list_cvalue, [zero, one], inbounds=True)
        return builder.load(ptr_to_head)

    def pprint(self, indent=0):
        return f'{indentation(indent)}tail of\n'+\
               self.expr.pprint(indent=indent+2)

    def __str__(self):
        return self.pprint()

class HeadOperator(Expression):
    def __init__(self, expr):
        self.expr = expr
        self.expr_type = None

    def sem(self, symbol_table):
        '''
            1) Checks that the given expression is a list and not BaseType.Nil

            2) Returns the type of the list
        '''

        t = self.expr.sem(symbol_table)

        self.expr_type = t

        if not isinstance(t, List):
            errormsg = f'Head operator can not be used with type {t}.'
            raise Exception(errormsg)

        return t.t # list subtype

    def codegen(self, module, builder, symbol_table):
        # self.expr will not be Nil - guaranteed by the semantics check
        # however, it might be an atom that points to an empty list.
        # in that case it will crach during execution

        list_cvalue = self.expr.codegen(module, builder, symbol_table)

        if should_load_or_store(self.expr, symbol_table):
            list_cvalue = builder.load(list_cvalue)

        zero = ir.Constant(LLVM_Types.Int, 0)

        ptr_to_head = builder.gep(list_cvalue, [zero, zero], inbounds=True)
        return builder.load(ptr_to_head)

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

    def codegen(self, module, builder, symbol_table):
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

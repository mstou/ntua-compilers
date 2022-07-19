from .node         import Node, indentation
from .symbol_table import *
from .data_types   import *
from .llvm_types   import *
from .atoms        import VarAtom
from .expressions  import AtomArray

from llvmlite import ir

class Statement(Node):
    ''' Generic class for statements '''
    pass

class ExitStatement(Statement):
    def __init__(self):
        pass

    def sem(self, symbol_table):
        return True

    def pprint(self, indent=0):
        return indentation(indent) + f'Exit()'

    def __str__(self):
        return self.pprint()

class SkipStatment(Statement):
    def __init__(self):
        pass

    def sem(self, symbol_table):
        return True

    def codegen(self, module, builder, symbol_table):
        '''
            The skip statement does nothing.
        '''
        return None

    def pprint(self, indent=0):
        return indentation(indent) + f'Skip()'

    def __str__(self):
        return self.pprint()


class ReturnStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

    def sem(self, symbol_table):
        return self.expr.sem(symbol_table)
        #TODO: check that we are inside a function that returns the type we return.

    def codegen(self, module, builder, symbol_table):
        expr_cvalue = self.expr.codegen(module, builder, symbol_table)
        return builder.ret(expr_cvalue)

    def pprint(self, indent=0):
        return indentation(indent) + f'Return\n'+\
               self.expr.pprint(indent+2)

    def __str__(self):
        return self.pprint()

class StatementList(Statement):
    def __init__(self, stmt, children):
        self.stmt     = stmt
        self.children = children

    def getStatements(self):
        return [] if self.stmt == None\
               else [self.stmt] + self.children.getStatements()

class IfStatement(Statement):
    def __init__(self, condition, statement, stmtlist):
        self.condition = condition
        self.statements = [statement] + stmtlist.getStatements()

    def sem(self, symbol_table):
        '''
            1) Checks that the condition is BaseType.Bool
            2) Calls the sem() of each statement
        '''
        t = self.condition.sem(symbol_table)
        if t != BaseType.Bool:
            errormsg = f'The condition of the if clause must be of type {BaseType.Bool}'
            raise Exception(errormsg)

        for s in self.statements:
            s.sem(symbol_table)

        return True

    def codegen(self, module, builder, symbol_table):
        cond = self.condition.codegen(module, builder, symbol_table)
        cmp  = builder.icmp_unsigned('!=', cond, ir.Constant(LLVM_Types.Bool, 0))

        then_bb  = builder.function.append_basic_block('then')
        after_bb = ir.Block(builder.function, 'after')
        builder.cbranch(cmp, then_bb, after_bb) # conditional branch

        # Building the 'then' block
        builder.position_at_start(then_bb)
        for s in self.statements:
            s.codegen(module, builder, symbol_table)

        builder.branch(after_bb)

        # then_bb = self.builder.block <- remember the block that then ends in
        # for the phi function

        builder.function.basic_blocks.append(after_bb)
        builder.position_at_start(after_bb)


    def pprint(self, indent=0):
        s = indentation(indent) + 'If Statement\n'
        s += indentation(indent+2) + 'Condition\n'
        s += self.condition.pprint(indent+4) + '\n'
        s += indentation(indent+2) + 'Statements\n'

        for i,stmt in enumerate(self.statements):
            s += stmt.pprint(indent+4)
            if i != len(self.statements)-1: s += '\n'

        return s

    def __str__(self):
        return self.pprint()


class ElseStatement(Statement):
    def __init__(self, statement, stmtlist):
        self.statements = [statement] + stmtlist.getStatements()

    def sem(self, symbol_table):
        '''
            Calls the sem() of each statement
        '''

        for s in self.statements:
            s.sem(symbol_table)

        return True

    def pprint(self, indent=0):
        s = indentation(indent) + 'Else Statement\n'
        s += indentation(indent+2) + 'Statements\n'

        for i,stmt in enumerate(self.statements):
            s += stmt.pprint(indent+4)
            if i != len(self.statements)-1: s += '\n'

        return s

    def __str__(self):
        return self.pprint()

class ElsifStatement(Statement):
    def __init__(self, condition, statement, stmtlist):
        self.condition  = condition
        self.statements = [statement] + stmtlist.getStatements()

    def sem(self, symbol_table):
        '''
            1) Checks that the condition is BaseType.Bool
            2) Calls the sem() of each statement
        '''
        t = self.condition.sem(symbol_table)
        if t != BaseType.Bool:
            errormsg = f'The condition of the if clause must be of type {BaseType.Bool}'
            raise Exception(errormsg)

        for s in self.statements:
            s.sem(symbol_table)

        return True

    def pprint(self, indent=0):
        s = indentation(indent) + 'ElseIf Statement\n'
        s += indentation(indent+2) + 'Condition\n'
        s += self.condition.pprint(indent+4) + '\n'
        s += indentation(indent+2) + 'Statements\n'

        for i,stmt in enumerate(self.statements):
            s += stmt.pprint(indent+4)
            if i != len(self.statements)-1: s += '\n'

        return s

    def __str__(self):
        return self.pprint()

class ElsifList(Statement):
    def __init__(self, elsif, children):
        self.elsif    = elsif
        self.children = children

    def getClauses(self):
        return [] if self.elsif == None\
               else [self.elsif] + self.children.getClauses()

class IfElsifStatement(Statement):
    def __init__(self, ifclause, elsiflist):
        self.ifclause = ifclause
        self.elsifs   = elsiflist.getClauses() # list of ElsifStatement

    def sem(self, symbol_table):
        '''
            Calls the sem() of all the clauses
        '''
        self.ifclause.sem(symbol_table)

        for eif in self.elsifs:
            eif.sem(symbol_table)

        return True

    def pprint(self, indent=0):
        s = self.ifclause.pprint(indent) + '\n'

        for i,e in enumerate(self.elsifs):
            s += e.pprint(indent)
            if i != len(self.elsifs)-1: s += '\n'

        return s

    def __str__(self):
        return self.pprint()

class IfElseStatement(Statement):
    def __init__(self, ifclause, else_clause):
        self.ifclause    = ifclause
        self.else_clause = else_clause

    def sem(self, symbol_table):
        '''
            Calls the sem() of all the clauses
        '''

        self.ifclause.sem(symbol_table)
        self.else_clause.sem(symbol_table)

        return True

    def codegen(self, module, builder, symbol_table):
        cond = self.ifclause.condition.codegen(module, builder, symbol_table)
        cmp  = builder.icmp_unsigned('!=', cond, ir.Constant(LLVM_Types.Bool, 0))

        then_bb  = builder.function.append_basic_block('then')
        else_bb  = ir.Block(builder.function, 'else')
        after_bb = ir.Block(builder.function, 'after')
        builder.cbranch(cmp, then_bb, else_bb) # conditional branch

        # Building the 'then' block
        builder.position_at_start(then_bb)
        for s in self.ifclause.statements:
            s.codegen(module, builder, symbol_table)
        builder.branch(after_bb)

        # Building the 'else' block
        builder.function.basic_blocks.append(else_bb)
        builder.position_at_start(else_bb)
        for s in self.else_clause.statements:
            s.codegen(module, builder, symbol_table)
        builder.branch(after_bb)

        builder.function.basic_blocks.append(after_bb)
        builder.position_at_start(after_bb)

    def pprint(self, indent=0):
        return self.ifclause.pprint(indent) +\
               '\n' + self.else_clause.pprint(indent)

    def __str__(self):
        return self.pprint()

class IfFullStatement(Statement):
    def __init__(self, ifclause, elsiflist, else_clause):
        self.ifclause    = ifclause
        self.else_clause = else_clause
        self.elsifs      = elsiflist.getClauses()


    def sem(self, symbol_table):
        '''
            Calls the sem() of all the clauses
        '''
        self.ifclause.sem(symbol_table)

        for eif in self.elsifs:
            eif.sem(symbol_table)

        self.else_clause.sem(symbol_table)

        return True

    def pprint(self, indent=0):
        s = self.ifclause.pprint(indent) + '\n'

        for e in self.elsifs:
            s += e.pprint(indent) + '\n'

        s += self.else_clause.pprint(indent)

        return s

    def __str__(self):
        return self.pprint()


class ForLoop(Statement):
    def __init__(self, initial, condition, ending, stmt, stmtlist):
        self.initial    = initial
        self.condition  = condition
        self.ending     = ending
        self.statements = [stmt] + stmtlist.getStatements()

    def sem(self, symbol_table):
        '''
            1) Calls sem() on the initial and ending simple list and all the
               statements
            2) Checks that the terminating condition is of type BaseType.Bool
        '''

        t = self.condition.sem(symbol_table)
        if t != BaseType.Bool:
            errormsg = f'The terminating condition of the for-loop must be of type {BaseType.Bool}'
            raise Exception(errormsg)

        self.initial.sem(symbol_table)
        self.ending.sem(symbol_table)

        for s in self.statements:
            s.sem(symbol_table)

        return True

    def pprint(self, indent=0):
        s = indentation(indent) + 'For Loop\n'

        s += indentation(indent+2) + 'Initial\n'
        s += self.initial.pprint(indent+4) + '\n'

        s += indentation(indent+2) + 'Condition\n'
        s += self.condition.pprint(indent+4) + '\n'

        s += indentation(indent+2) + 'Ending\n'
        s += self.ending.pprint(indent+4) + '\n'

        s += indentation(indent+2) + 'Statements\n'

        for i,stmt in enumerate(self.statements):
            s += stmt.pprint(indent+4)
            if i != len(self.statements)-1: s += '\n'

        return s


    def __str__(self):
        return self.pprint()

class FunctionCall(Statement):
    def __init__(self, name, expressions):
        self.name = name
        self.expressions = expressions

    def sem(self, symbol_table):
        '''
            1) Checks that the function exists
            2) Checks that all the parameters are of the expected type
            3) Checks that parameters passed by reference are l-values
        '''

        # TODO 3


        f = symbol_table.lookup(self.name)

        if f == None:
            errormsg = f'Function {self.name} is not defined'
            raise Exception(errormsg)

        if not isinstance(f, FunctionEntry):
            errormsg = f'{self.name} is not a function'
            raise Exception(errormsg)

        params = f.params

        for e, param in zip(self.expressions,params):
            expected_type = param[1]
            actual_type = e.sem(symbol_table)

            if expected_type != actual_type:
                errormsg = f'Expected a parameter of type {expected_type} ' +\
                           f'but got {actual_type} instead'
                raise Exception(errormsg)

        return f.return_type

    def codegen(self, module, builder, symbol_table):
        func_cvalue = symbol_table.lookup(self.name).cvalue
        params = []

        for e in self.expressions:
            p = e.codegen(module, builder, symbol_table)
            val = p
            if isinstance(e, VarAtom):
                entry = symbol_table.lookup(e.name)
                if not isinstance(entry, FunctionParam):
                    val = builder.load(p)

            params.append(val)


        return builder.call(func_cvalue, params)

    def pprint(self, indent=0):
        s = indentation(indent) + 'Function Call\n'
        s += indentation(indent+2) + f'Function Name: {self.name}\n'
        s += indentation(indent+2) + 'Parameters\n'

        for i,e in enumerate(self.expressions):
            s += indentation(indent+4) + f'Parameter {i+1}\n'
            s += e.pprint(indent+6)
            if i != len(self.expressions)-1: s += '\n'

        return s

    def __str__(self):
        return self.pprint()

class Assignment(Statement):
    def __init__(self, atom, expr):
        self.atom = atom
        self.expr = expr

    def sem(self, symbol_table):
        '''
            1) Checks that the atom is a variable name
            2) Checks that the variable is already defined and has the
               same type with the given expression
        '''

        expr_type = self.expr.sem(symbol_table)

        if not isinstance(self.atom, VarAtom) and not isinstance(self.atom, AtomArray):
            errormsg = f'The left-hand side of an assignment can only be a variable.'
            raise Exception(errormsg)

        var_type = self.atom.sem(symbol_table)

        if var_type != expr_type:
            errormsg = f'Unsupported assignment between {var_type} and {expr_type}'
            raise Exception(errormsg)

        return True

    def codegen(self, module, builder, symbol_table):
        atom_cvalue = self.atom.codegen(module, builder, symbol_table) # performs a lookup and returns the cvalue
        expr_cvalue = self.expr.codegen(module, builder, symbol_table)

        builder.store(expr_cvalue, atom_cvalue)

        return None

    def pprint(self, indent=0):
        s = indentation(indent) + 'Assignment\n'
        s += indentation(indent+2) + f'Name: {self.atom}\n'
        s += indentation(indent+2) + 'Expression\n'
        s += self.expr.pprint(indent+4)

        return s

    def __str__(self):
        return self.pprint()

class SimpleListComma(Statement):
    def __init__(self, simple, simplelistcomma):
        self.simple = simple
        self.simplelistcomma = simplelistcomma

    def getSimples(self):
        return [] if self.simple == None\
        else [self.simple] + self.simplelistcomma.getSimples()

class SimpleList(Statement):
    def __init__(self, simples):
        self.simples = simples

    def sem(self, symbol_table):
        '''
            Calls the sem() function on all the simples
        '''
        for s in self.simples:
            s.sem(symbol_table)

        return True

    def pprint(self, indent=0):
        s = indentation(indent) + 'List of Simples\n'

        for i,sim in enumerate(self.simples):
            s += sim.pprint(indent+2)
            if i != len(self.simples)-1: s += '\n'

        return s

    def __str__(self):
        return self.pprint()

from .node         import Node, indentation
from .symbol_table import *
from .data_types   import *
from .llvm_types   import *
from .atoms        import VarAtom
from .expressions  import AtomArray, should_load_or_store

from llvmlite import ir

class Statement(Node):
    ''' Generic class for statements '''
    pass

class ExitStatement(Statement):
    def __init__(self):
        pass

    def sem(self, symbol_table):
        function_scope = symbol_table.get_scope_name()
        entry = symbol_table.lookup(function_scope)

        if function_scope == None or entry == None or not isinstance(entry, FunctionEntry):
            errormsg = f'Return statement in wrong scope'
            raise Exception(errormsg)

        expected_type = entry.return_type

        if entry.return_type != BaseType.Void:
            errormsg = f'Exit statement in non-void function. Expected to '+\
                       f'return a value of type {entry.return_type}'
            raise Exception(errormsg)

        return True

    def codegen(self, module, builder, symbol_table):
        builder.ret_void()

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
        type = self.expr.sem(symbol_table)

        function_scope = symbol_table.get_scope_name()

        entry = symbol_table.lookup(function_scope)

        if function_scope == None or entry == None or not isinstance(entry, FunctionEntry):
            errormsg = f'Return statement in wrong scope'
            raise Exception(errormsg)

        expected_type = entry.return_type

        if entry.return_type == BaseType.Void:
            errormsg = f'Return statement in void function'
            raise Exception(errormsg)

        if entry.return_type != type:
            errormsg = f'Wrong return type inside function {function_scope}. '+\
                       f'Expected {entry.return_type} but got {type} instead.'

        symbol_table.register_return_statement()

        return True

    def codegen(self, module, builder, symbol_table):
        expr_cvalue = self.expr.codegen(module, builder, symbol_table)

        if should_load_or_store(self.expr, symbol_table):
                expr_cvalue = builder.load(expr_cvalue)

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

        if should_load_or_store(self.condition, symbol_table):
            cond = builder.load(cond)

        cmp  = builder.icmp_unsigned('!=', cond, ir.Constant(LLVM_Types.Bool, 0))

        then_bb  = builder.function.append_basic_block('then')
        after_bb = ir.Block(builder.function, 'after')
        builder.cbranch(cmp, then_bb, after_bb) # conditional branch

        # Building the 'then' block
        builder.position_at_start(then_bb)
        for s in self.statements:
            s.codegen(module, builder, symbol_table)

        if not builder.block.is_terminated: builder.branch(after_bb)

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

        if should_load_or_store(self.ifclause.condition, symbol_table):
            cond = builder.load(cond)

        cmp  = builder.icmp_unsigned('!=', cond, ir.Constant(LLVM_Types.Bool, 0))

        then_bb  = builder.function.append_basic_block('then')
        else_bb  = ir.Block(builder.function, 'else')
        after_bb = ir.Block(builder.function, 'after')
        builder.cbranch(cmp, then_bb, else_bb) # conditional branch

        # Building the 'then' block
        builder.position_at_start(then_bb)
        for s in self.ifclause.statements:
            s.codegen(module, builder, symbol_table)
        if not builder.block.is_terminated: builder.branch(after_bb)

        # Building the 'else' block
        builder.function.basic_blocks.append(else_bb)
        builder.position_at_start(else_bb)
        for s in self.else_clause.statements:
            s.codegen(module, builder, symbol_table)
        if not builder.block.is_terminated: builder.branch(after_bb)

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

    def codegen(self, module, builder, symbol_table):
        FALSE = ir.Constant(LLVM_Types.Bool, 0)
        cond = self.ifclause.condition.codegen(module, builder, symbol_table)

        if should_load_or_store(self.ifclause.condition, symbol_table):
            cond = builder.load(cond)

        cmp  = builder.icmp_unsigned('!=', cond, FALSE)

        then_bb  = builder.function.append_basic_block('then')
        else_bb  = ir.Block(builder.function, 'else')
        after_bb = ir.Block(builder.function, 'after')
        elsif_conds = []
        elsif_bb = []

        for i,_ in enumerate(self.elsifs):
            elsif_conds.append(ir.Block(builder.function, f'elsif_cond_{i}'))
            elsif_bb.append(ir.Block(builder.function, f'elsif_bb_{i}'))

        builder.cbranch(cmp, then_bb, elsif_conds[0]) # conditional branch for first if

        # Building the 'then' block
        builder.position_at_start(then_bb)
        for s in self.ifclause.statements:
            s.codegen(module, builder, symbol_table)
        if not builder.block.is_terminated: builder.branch(after_bb)

        # Building all the elsif blocks
        for i, eif in enumerate(self.elsifs):
            builder.function.basic_blocks.append(elsif_conds[i])
            builder.position_at_start(elsif_conds[i])
            cond = eif.condition.codegen(module, builder, symbol_table)

            if should_load_or_store(eif.condition, symbol_table):
                cond = builder.load(cond)

            cmp  = builder.icmp_unsigned('!=', cond, FALSE)

            if i == len(self.elsifs) - 1:
                next = else_bb
            else:
                next = elsif_conds[i+1]

            builder.cbranch(cmp, elsif_bb[i], next)

            builder.function.basic_blocks.append(elsif_bb[i])
            builder.position_at_start(elsif_bb[i])
            for s in eif.statements:
                s.codegen(module, builder, symbol_table)
            if not builder.block.is_terminated: builder.branch(after_bb)

        # Building the 'else' block
        builder.function.basic_blocks.append(else_bb)
        builder.position_at_start(else_bb)
        for s in self.else_clause.statements:
            s.codegen(module, builder, symbol_table)
        if not builder.block.is_terminated: builder.branch(after_bb)


        builder.function.basic_blocks.append(after_bb)
        builder.position_at_start(after_bb)

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

    def codegen(self, module, builder, symbol_table):

        # creating the basic blocks
        loopcond  = ir.Block(builder.function, 'loopcond')
        loopbody  = ir.Block(builder.function, 'loopbody')
        afterloop = ir.Block(builder.function, 'afterloop')

        # codegen the initial statements and branch to loop condition
        self.initial.codegen(module, builder, symbol_table)
        builder.branch(loopcond)

        # building the loop condition and branch in body or after the loop
        builder.function.basic_blocks.append(loopcond)
        builder.position_at_start(loopcond)
        cond = self.condition.codegen(module, builder, symbol_table)

        if should_load_or_store(self.condition, symbol_table):
            cond = builder.load(cond)

        cmp  = builder.icmp_unsigned('!=', cond, ir.Constant(LLVM_Types.Bool, 0))
        builder.cbranch(cmp, loopbody, afterloop)

        # building the loop body
        builder.function.basic_blocks.append(loopbody)
        builder.position_at_start(loopbody)
        for s in self.statements:
            s.codegen(module, builder, symbol_table)
        self.ending.codegen(module, builder, symbol_table)
        builder.branch(loopcond)

        # basic block after the loop
        builder.function.basic_blocks.append(afterloop)
        builder.position_at_start(afterloop)

        return None

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

        if len(params) != len(self.expressions):
            errormsg = f'Wrong number of arguments provided for function {self.name}'+\
                       f'Expected {len(params)} parameters but got {len(self.expressions)}'

            raise Exception(errormsg)

        for e, param in zip(self.expressions,params):
            expected_type = param[1]
            actual_type = e.sem(symbol_table)

            if expected_type != actual_type:
                errormsg = f'Expected a parameter of type {expected_type} ' +\
                           f'but got {actual_type} instead'
                raise Exception(errormsg)

        return f.return_type

    def codegen(self, module, builder, symbol_table):
        function_entry = symbol_table.lookup(self.name)
        func_cvalue    = function_entry.cvalue

        params = []

        for e, exp_param in zip(self.expressions, function_entry.params):
            # passing the normal parameters
            p = e.codegen(module, builder, symbol_table)
            val = p
            by_ref = exp_param[2]

            if should_load_or_store(e, symbol_table) and not by_ref:
                val = builder.load(p)

            params.append(val)

        typical_params = len(self.expressions)

        for p in function_entry.params[typical_params:]:
            # passing the extra hidden llvm parameters
            n, t, ref = p
            entry = symbol_table.lookup(n)
            cvalue = entry.cvalue

            # the hidden params are all passed by reference, hence we should not
            # load from the pointers

            params.append(cvalue)

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
        self.atom_type = None
        self.expr_type = None

    def sem(self, symbol_table):
        '''
            1) Checks that the atom is a variable name
            2) Checks that the variable is already defined and has the
               same type with the given expression
        '''

        expr_type = self.expr.sem(symbol_table)
        self.expr_type = expr_type

        if not isinstance(self.atom, VarAtom) and not isinstance(self.atom, AtomArray):
            errormsg = f'The left-hand side of an assignment can only be a variable.'
            raise Exception(errormsg)

        var_type = self.atom.sem(symbol_table)
        self.atom_type = var_type

        if var_type != expr_type:
            errormsg = f'Unsupported assignment between {var_type} and {expr_type}'
            raise Exception(errormsg)

        return True

    def codegen(self, module, builder, symbol_table):
        atom_cvalue = self.atom.codegen(module, builder, symbol_table) # performs a lookup and returns the cvalue

        if isinstance(self.atom_type, List) and isinstance(self.expr_type, BaseType): # expr = Nil
            expr_cvalue = self.expr.codegen(module, builder, symbol_table, type=self.atom_type)
        else:
            expr_cvalue = self.expr.codegen(module, builder, symbol_table)

        if should_load_or_store(self.expr, symbol_table):
            expr_cvalue = builder.load(expr_cvalue)

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

    def codegen(self, module, builder, symbol_table):
        for s in self.simples:
            s.codegen(module, builder, symbol_table)

        return None

    def pprint(self, indent=0):
        s = indentation(indent) + 'List of Simples\n'

        for i,sim in enumerate(self.simples):
            s += sim.pprint(indent+2)
            if i != len(self.simples)-1: s += '\n'

        return s

    def __str__(self):
        return self.pprint()

from .node         import Node, indentation
from .symbol_table import *
from .llvm_types   import BaseType_to_LLVM
from llvmlite      import ir

class FuncDef(Node): # function definition
    def __init__(self, header, funcdefhelp, stmt, stmtlist):
        self.header      = header      # type FunctionHeader
        self.funcdefhelp = funcdefhelp # type FuncDefHelp
        self.stmt        = stmt        # type Statement
        self.stmtlist    = stmtlist

        self.vardefs   = []
        self.funcdefs  = []
        self.funcdecls = []

        for _def in self.funcdefhelp.getDefinitions():
            t = _def.statement_type

            if t == 'funcdecl':
                self.funcdecls.append(_def.d)
            elif t == 'funcdef':
                self.funcdefs.append(_def.d)
            elif t == 'vardef':
                self.vardefs.append(_def.d)

        self.statements = [self.stmt] + self.stmtlist.getStatements()

    def sem(self, symbol_table):
        '''
            1) Calls the sem() function of the header declaring that it is
            a function definition
            2) Calls the sem of the rest of the components
        '''

        self.header.sem(symbol_table, decl=False)

        for v in self.vardefs:
            v.sem(symbol_table)

        for decl in self.funcdecls:
            decl.sem(symbol_table)

        for f_def in self.funcdefs:
            f_def.sem(symbol_table)

        for stmt in self.statements:
            stmt.sem(symbol_table)

        symbol_table.closeScope()
        #TODO: check that there are no functions that are declared and not implemented in the closed scope

        return True

    def codegen(self, module, builder, symbol_table, main=False):
        '''
            1) Calls the codegen() function of the header to register the function,
            open a new scope in the symbol table and insert all the parameters.

            2) Creates a new block which is the function's entry block

            3) Changes the builder to write in the function's entry block and
            calls the codegen() of all the statements
        '''

        func = self.header.codegen(module, builder, symbol_table)

        entry_block = func.append_basic_block(f'{self.header.function_name}_entry')

        if main:
            builder = ir.IRBuilder(entry_block)

        with builder.goto_block(entry_block):
            for v in self.vardefs:
                v.codegen(module, builder, symbol_table)

            for decl in self.funcdecls:
                decl.codegen(module, builder, symbol_table)

            for f_def in self.funcdefs:
                f_def.codegen(module, builder, symbol_table)

            for stmt in self.statements:
                stmt.codegen(module, builder, symbol_table)
                #TODO: check the return statement and add ret_void for void functions

            if self.header.return_type_llvm == BaseType_to_LLVM(BaseType.Void):
                builder.ret_void()
            symbol_table.closeScope()

        return func

    def pprint(self, indent=0):
        s  = indentation(indent)
        s += 'Function Definition\n'
        s += self.header.pprint(indent+2)

        if len(self.vardefs) > 0:
            s += indentation(indent+2) + 'Variable definitions:\n'
            for var in self.vardefs:
                s += var.pprint(indent+4) + '\n'

        if len(self.funcdecls) > 0:
            s += indentation(indent+2) + 'Function Declarations:\n'
            for decl in self.funcdecls:
                s += decl.pprint(indent+4) + '\n'

        if len(self.funcdefs) > 0:
            s += indentation(indent+2) + 'Function Definitions:\n'
            for d in self.funcdefs:
                s += d.pprint(indent+4) + '\n'

        s += indentation(indent+2) + 'Statements:\n'

        for i,stmt in enumerate(self.statements):
            s += stmt.pprint(indent+4)
            if i != len(self.statements)-1: s += '\n'

        return s

    def __str__(self):
        return self.pprint()


class FuncDecl(Node): # function definition
    def __init__(self, header):
        self.header = header

    def sem(self, symbol_table):
        return self.header.sem(symbol_table,decl = True)

    def codegen(self, module, builder, symbol_table):
        return self.header.codegen(module, builder, symbol_table)

    def pprint(self, indent=0):
        s = indentation(indent)
        s += f'Function Declaration:\n'
        s += self.header.pprint(indent+2)
        return s

    def __str__(self):
        return self.pprint()

class FuncDefHelp(Node): # function definitions recursively
    def __init__(self, d, child):
        self.d = d
        self.child = child

    def getDefinitions(self):
        return [] if self.d == None\
               else [self] + self.child.getDefinitions()

class FuncDefHelp_FuncDecl(FuncDefHelp):
    def __init__(self, d, child):
        super().__init__(d, child)
        self.statement_type = 'funcdecl'


class FuncDefHelp_FuncDef(FuncDefHelp):
    def __init__(self, d, child):
        super().__init__(d, child)
        self.statement_type = 'funcdef'


class FuncDefHelp_VarDef(FuncDefHelp):
    def __init__(self, d, child):
        super().__init__(d, child)
        self.statement_type = 'vardef'


class FunctionHeader(Node):
    def __init__(self, type, name, formal, formallist, decl=False):
        self.function_type = type
        self.function_name = name

        self.all_formals = [] if formal == None else\
                           [formal] + formallist.getFormals()
        self.params = []
        for f in self.all_formals:
            for name in f.names:
                self.params.append((name, f.type, f.reference))


    def sem(self, symbol_table, decl = False):
        '''
        We may have arrived here either from a declaration or
        from a function definition.

        In the case of a function declaration:
            1a) We check that the function has not already been declared
            1b) We add the function to the symbol table and label it undefined

        In the case of a function definition:
            2a) If a symbol entry exists, we check that the function is undefined,
                hence the entry was produced from a declaration
            2b) We create (or modify) an entry for the function in the current scope
               (which is the global scope, or one above the function scope).
            2c) We open a new scope and insert all the parameters of the function

        In any case we also check that the names of the parameters are correct,
        i.e. two parameters can not share the same name
        '''

        param_names = set()
        for p in self.params:
            name, _, _ = p
            if name in param_names:
                errormsg = f'Two or more parameters share the name {name}'
                raise Exception(errormsg)
            param_names.add(name)

        parameters = []
        for p in self.params:
            name, t, ref = p
            type = t.sem(symbol_table) # calculate the actual type
            parameters.append((name,type,ref))

        return_type = self.function_type.sem(symbol_table)
        self.return_type_llvm = BaseType_to_LLVM(return_type)

        entry = symbol_table.lookup(self.function_name)
        if decl:
            errormsg = f'Tried to declare a function with name {self.name} ' +\
                        'but the name is already in use.'
            raise Exception(errormsg)

            new_entry = FunctionEntry(self.function_name,\
                        return_type, parameters, defined=False\
                        )
            symbol_table.insert(self.function_name, new_entry)
            return True

        else:
            if entry != None and not isinstance(entry, FunctionEntry):
                errormsg = f'Tried to define a function with name {self.name} ' +\
                            'but the name is already in use.'
                raise Exception(errormsg)

            if entry != None and entry.defined:
                errormsg = f'A function with name {self.name} ' +\
                            'has already been defined.'
                raise Exception(errormsg)

            if entry != None and not entry.defined:
                entry.defined = True

            else:
                new_entry = FunctionEntry(self.function_name,\
                            return_type, parameters, defined=True\
                            )
                symbol_table.insert(self.function_name, new_entry)

                symbol_table.openScope()

                for n,t,ref in self.params:
                    type = t.sem(symbol_table)
                    symbol_table.insert(n, FunctionParam(n,type,ref))

            return True

    def codegen(self, module, builder, symbol_table, decl = False):
        '''
            We may have arrived here either from a declaration or
            from a function definition.

            In the case of a function declaration:
                We know that the function has not already been declared from the semantics check.
                -> We add the function to the symbol table and label it undefined

            In the case of a function definition:
                We know that this is the only definition of the function from the semantics check.
                -> We add the function to the symbol table if it has not already been declared
                -> We add a function definition in the module
                -> We open a new scope and insert all the parameters of the function
        '''

        if not decl:
            func_cvalue = symbol_table.lookup(self.function_name)

        if func_cvalue == None or decl:
            # the function is about to be declared or about to be defined and was
            # not previously declared.
            # declare the function type and add it to the scope
            parameters = [BaseType_to_LLVM(p[1]) for p in self.params]
            ret_type   = self.return_type_llvm
            func_type = ir.FunctionType(ret_type, parameters)
            func_cvalue = ir.Function(module, func_type, name=self.function_name)

            symbol_table.insert(self.function_name,
                FunctionEntry(
                    self.function_name,
                    self.function_type,
                    self.params,
                    defined = not decl,
                    cvalue = func_cvalue
                )
            )

        if not decl:
            # begining the definition

            # we open a new scope in the symbol table
            symbol_table.openScope()

            # register all the arguments
            for i, arg in enumerate(func_cvalue.args):
                n, t, ref = self.params[i]
                cvalue = arg
                symbol_table.insert(n, FunctionParam(n,type,ref,cvalue=cvalue))
                # TODO: t is not a BaseType, change all nodes to save their llvm type in a variable
                # TODO: implement reference variables

        return func_cvalue

    def pprint(self, indent=0):
        s = f'{indentation(indent)}Function Header\n'+\
            f'{indentation(indent+2)}Name: {self.function_name}\n'+\
            f'{indentation(indent+2)}Return Type: {self.function_type}\n'+\
            f'{indentation(indent+2)}Variables:'+\
            f'{"NONE" if len(self.all_formals) == 0 else ""}\n'

        for i,formal in enumerate(self.all_formals):
            s += indentation(indent+4)
            s += f'{"REF " if formal.reference else ""}'
            s += f'{formal.type} '
            s += ', '.join(formal.names)
            s += '\n'

        return s

    def __str__(self):
        return self.pprint()


class Formal(Node): # variable declaration in function header
    def __init__(self, vardef, reference):
        self.reference = reference
        self.vardef = vardef
        self.names  = vardef.names
        self.type   = vardef.type

class FormalList(Node):
    def __init__(self, formal, child):
        self.formal = formal
        self.child = child

    def getFormals(self):
        return [] if self.formal == None else\
               [self.formal] + self.child.getFormals()

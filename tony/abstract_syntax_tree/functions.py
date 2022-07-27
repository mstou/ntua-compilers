from .node         import Node, indentation
from .symbol_table import *
from .llvm_types   import BaseType_to_LLVM
from .data_types   import List
from .statements   import ExitStatement
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

        return_type = self.header.sem(symbol_table, decl=False)

        for v in self.vardefs:
            v.sem(symbol_table)

        for decl in self.funcdecls:
            decl.sem(symbol_table)

        for f_def in self.funcdefs:
            f_def.sem(symbol_table)

        for stmt in self.statements:
            stmt.sem(symbol_table)

        if not symbol_table.all_funcs_defined():
            errormsg = 'Some functions were declared but not defined'
            raise Exception(errormsg)

        if return_type != BaseType.Void and not symbol_table.scope_has_returned():
            errormsg = f'No return statement inside non-void function {self.header.function_name}'
            raise Exception(errormsg)

        global_accesses = symbol_table.get_global_accesses()
        extra_params = []

        for entry in global_accesses:
            name_ = entry.name
            type_ = BaseType_to_LLVM(entry.type, var_definition = True).as_pointer()
            ref_ = True

            extra_params.append((name_, type_, ref_))

        self.header.extra_accesses = extra_params

        symbol_table.closeScope()

        return True

    def codegen(self, module, builder, symbol_table, main=False):
        '''
            1) Calls the codegen() function of the header to register the function,
            open a new scope in the symbol table and insert all the parameters.

            2) Creates a new block which is the function's entry block

            3) Changes the builder to write in the function's entry block and
            calls the codegen() of all the statements
        '''

        func = self.header.codegen(module, builder, symbol_table, main=main)

        entry_block = func.append_basic_block(f'{self.header.function_name}_entry')

        if main:
            builder = ir.IRBuilder(entry_block)

        with builder.goto_block(entry_block):

            self.allocate_parameters(builder, symbol_table)

            for v in self.vardefs:
                v.codegen(module, builder, symbol_table)

            for decl in self.funcdecls:
                decl.codegen(module, builder, symbol_table)

            for f_def in self.funcdefs:
                f_def.codegen(module, builder, symbol_table)

            for stmt in self.statements:
                stmt.codegen(module, builder, symbol_table)
                if isinstance(stmt, ExitStatement):
                    break

            if self.header.return_type_llvm == BaseType_to_LLVM(BaseType.Void):
                if not builder.block.is_terminated:
                    builder.ret_void()

            elif len(builder.block.instructions) == 0:
                # empty block and hence unreachable
                builder.unreachable()

            symbol_table.closeScope()

        return func

    def allocate_parameters(self, builder, symbol_table):
        all_params = self.header.actual_llvm_params

        for p in all_params:
            n, t, ref = p
            if ref: continue

            entry = symbol_table.lookup(n)
            old_cvalue = entry.cvalue

            new_cvalue = builder.alloca(t)
            builder.store(old_cvalue, new_cvalue)

            entry.cvalue = new_cvalue

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

        self.return_type_llvm = None
        self.param_types_llvm = []

        self.extra_accesses = []
        self.name_prefix = ''

    def sanitize(self, name):
        '''
            This is a function name sanitizer because x86 complains
            about the use of english question marks in names
        '''

        new_name = name

        if '?' in name:
            new_name = '_' + name.replace('?','_')

        return new_name

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

            llvm_type = BaseType_to_LLVM(type, var_definition = True)
            if ref:
                llvm_type = llvm_type.as_pointer()

            self.param_types_llvm.append(llvm_type)

        return_type = self.function_type.sem(symbol_table)
        self.return_type_llvm = BaseType_to_LLVM(return_type, var_definition = True)

        entry = symbol_table.lookup(self.function_name)
        if decl:

            if entry != None:
                errormsg = f'Tried to declare a function with name {self.function_name} ' +\
                            'but the name is already in use.'
                raise Exception(errormsg)

            new_entry = FunctionEntry(self.function_name,\
                        return_type, parameters, defined=False\
                        )
            symbol_table.insert(self.function_name, new_entry)
            return return_type

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

            symbol_table.openScope(self.function_name)

            for n,t,ref in self.params:
                type = t.sem(symbol_table)
                symbol_table.insert(n, FunctionParam(n,type,ref))

            return return_type

    def codegen(self, module, builder, symbol_table, decl = False, main = False):
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

        self.actual_llvm_params = []
        for p, llvm_t in zip(self.params, self.param_types_llvm):
            n, _, ref = p
            self.actual_llvm_params.append((n,llvm_t,ref))

        self.actual_llvm_params = self.actual_llvm_params + self.extra_accesses

        self.name_prefix = symbol_table.get_all_scope_names()

        if not decl:
            function_entry = symbol_table.lookup(self.function_name)
            if function_entry != None:
                func_cvalue = function_entry.cvalue

        if function_entry == None or decl:
            # the function is about to be declared or about to be defined and was
            # not previously declared.
            # declare the function type and add it to the scope
            parameters = [p[1] for p in self.actual_llvm_params] # llvm IR needs only the types
            ret_type   = self.return_type_llvm
            func_type = ir.FunctionType(ret_type, parameters)

            if main:
                llvm_name = 'main'
            else:
                llvm_name = self.sanitize(f'{self.name_prefix}_{self.function_name}')

            func_cvalue = ir.Function(module, func_type, name=llvm_name)

            symbol_table.insert(self.function_name,
                FunctionEntry(
                    self.function_name,
                    self.function_type,
                    self.actual_llvm_params,
                    defined = not decl,
                    cvalue = func_cvalue
                )
            )

        if not decl:
            # begining the definition

            # we open a new scope in the symbol table
            symbol_table.openScope(name=self.function_name)

            # register all the arguments
            for i, arg in enumerate(func_cvalue.args):
                n, t, ref = self.actual_llvm_params[i]
                cvalue = arg
                symbol_table.insert(n, FunctionParam(n,t,ref,cvalue=cvalue))

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

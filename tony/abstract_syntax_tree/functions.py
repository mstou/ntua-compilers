from .node import Node, indentation

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

    def sem(self, symbol_table):
        pass


class FuncDecl(Node): # function definition
    def __init__(self, header):
        self.header = header

    def sem(self, symbol_table):
        return self.header.sem(symbol_table)
    
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
            param_names.insert(name)


        entry = symbol_table.lookup(self.function_name)
        if decl:
            errormsg = f'Tried to declare a function with name {self.name} ' +\
                        'but the name is already in use.'
            raise Exception(errormsg)

            new_entry = Function(self.function_name, self.function_type, self.params)
            symbol_table.insert(self.function_name, new_entry, defined=False)

            return True

        else:
            if entry != None and not isinstance(entry, Function.__class__):
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
                new_entry = Function(self.function_name, self.function_type, self.params)
                symbol_table.insert(self.function_name, new_entry, defined=True)

                symbol_table.openScope()

                for n,t,ref in params:
                    symbol_table.insert(n, FunctionParam(n,t,ref))

            return True

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

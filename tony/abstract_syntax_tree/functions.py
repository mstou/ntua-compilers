from .node import Node

class FuncDef(Node): # function definition
    def __init__(self, header, functions, stmt, stmtlist):
        self.header = header       # type FunctionHeader
        self.functions = functions # type FuncDefHelp
        self.stmt = stmt           # type Statement
        self.stmtlist = stmtlist   # type

    def sem(self, symbol_table):
        pass


class FuncDecl(Node): # function definition
    def __init__(self, header):
        self.header = header       # type FunctionHeader

class FuncDefHelp(Node): # function definitions recursively
    def __init__(self, d, child):
        self.d = d
        self.child = child

class FuncDefHelp_FuncDecl(FuncDefHelp):
    def __init__(self, d, child):
        super().__init__(d, help)


class FuncDefHelp_FuncDef(FuncDefHelp):
    def __init__(self, d, child):
        super().__init__(d, help)


class FuncDefHelp_VarDef(FuncDefHelp):
    def __init__(self, d, child):
        super().__init__(d, help)


class FunctionHeader(Node):
    def __init__(self, type, name, formal, formallist):
        self.funtion_type = type
        self.function_name = name

        self.all_formals = [] if formal == None else\
                           [formal] + formallist.getFormals()

    def sem(self, symbol_table):
        '''
        1) Inserts the function with its type to the current scope
           after checking that the name is not already used

        2) Opens a new function scope

        3) Inserts all the variables in the scope and
           checks that there are no duplicates (e.g. the same
           name given for two or more parameters)
        '''

        if symbol_table.lookup(self.function_name) != None:
            error_msg = f'Syntax error. Tried to define a function\
            name {self.function_name}, but {self.function_name} is\
            already in use'

            raise Exception(error_msg)

        symbol_table.insert(name, Type.Function)

        # TODO: 2,3



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

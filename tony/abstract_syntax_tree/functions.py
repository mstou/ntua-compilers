from .node import Node

class FuncDef(Node): # function definition
    def __init__(self, header, functions, stmt, stmtlist):
        self.header = header       # type FunctionHeader
        self.functions = functions # type FuncDefHelp
        self.stmt = stmt           # type Statement
        self. stmtlist = stmtlist  # type

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
        self.type = type
        self.name = name
        self.formal = formal
        self.formallist = formallist


class Formal(Node): # variable declaration in function header
    def __init__(self, vardef, reference):
        self.reference = reference
        self.vardef = vardef

class FormalList(Node):
    def __init__(self, formal, child):
        self.formal = formal
        self.child = child

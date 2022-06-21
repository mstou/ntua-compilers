import re

class Node:
    def __init__(self, type, value, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []


    def __str__(self, depth=1):
        return_string = [re.sub('\n', lambda _: '\\n', str(self.value))]
        for child in self.children:
            return_string.extend(["\n", "  " * (depth+1), child.__str__(depth+1)])
        return "".join(return_string)


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

class Type(Node):
    ''' General Class for Data Types '''
    pass

class Int(Type):
    def __init__(self, data):
        self.data = data

class Bool(Type):
    def __init__(self, data):
        self.data = data

class Char(Type):
    def __init__(self, data):
        self.data = data

class VariableDefinition(Node):
    def __init__(self, type, name, vars):
        self.type = type
        self.name = name
        self.vars = vars

class Name(Node):
    def __init__(self, name):
        self.name = name

class NameList(Node):
    def __init__(self, name, names):
        self.name  = name
        self.names = names


#======== Map function =======
def mapTree(node, f):
    newType = node.type
    newValue = f(node.value)
    newChildren = []
    for child in node.children:
        newChildren.append(mapTree(child, f))

    return Node(newType, newValue, newChildren)


# t = Node('BinExpress', '+', [Node('NUMBER', 1), Node('NUMBER', 2)])
# print(t)

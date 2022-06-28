from .node import Node, indentation

class Statement(Node):
    ''' Generic class for statements '''
    pass

class ExitStatement(Statement):
    def __init__(self):
        pass

    def pprint(self, indent=0):
        return indentation(indent) + f'Exit()'

    def __str__(self):
        return self.pprint()

class SkipStatment(Statement):
    def __init__(self):
        pass

    def pprint(self, indent=0):
        return indentation(indent) + f'Skip()'

    def __str__(self):
        return self.pprint()


class ReturnStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

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
        self.statement = statement
        self.stmtlist  = stmtlist

class ElseStatement(Statement):
    def __init__(self, statement, stmtlist):
        self.statement = statement
        self.stmtlist  = stmtlist

class ElsifStatement(Statement):
    def __init__(self, condition, statement, stmtlist):
        self.condition = condition
        self.statement = statement
        self.stmtlist  = stmtlist

class ElsifList(Statement):
    def __init__(self, elsif, children):
        self.elsif    = elsif
        self.children = children

class IfElsifStatement(Statement):
    def __init__(self, ifclause, elsiflist):
        self.ifclause  = ifclause
        self.elsiflist = elsiflist

class IfElseStatement(Statement):
    def __init__(self, ifclause, else_clause):
        self.ifclause    = ifclause
        self.else_clause = else_clause

class IfFullStatement(Statement):
    def __init__(self, ifclause, elsiflist, else_clause):
        self.ifclause    = ifclause
        self.else_clause = else_clause
        self.elsiflist   = elsiflist

class ForLoop(Statement):
    def __init__(self, initial, condition, ending, stmt, stmtlist):
        self.initial   = initial
        self.condition = condition
        self.ending    = ending
        self.stmt      = stmt
        self.stmtlist  = stmtlist

class FunctionCall(Statement):
    def __init__(self, name, expressions):
        self.name = name
        self.expressions = expressions

class Assignment(Statement):
    def __init__(self, atom, expr):
        self.atom = atom
        self.expr = expr

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

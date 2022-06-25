from .node import Node

class Statement(Node):
    ''' Generic class for statements '''
    pass

class ExitStatement(Statement):
    def __init__(self):
        pass

class SkipStatment(Statement):
    def __init__(self):    
        pass

class ReturnStatement(Statement):
    def __init__(self, expr):
        self.expr = expr

class StatementList(Statement):
    def __init__(self, stmt, children):
        self.stmt     = stmt
        self.children = children

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
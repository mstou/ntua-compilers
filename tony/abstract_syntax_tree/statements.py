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
        self.statements = [statement] + stmtlist.getStatements()

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

from enum import Enum

class Type(Enum):
   INT  = 1
   CHAR = 2
   BOOL = 3
   VOID = 4
   NIL  = 5

class SymbolEntry:
    def __init__(self, type):
        self.type = type
    def __str__(self):
        return str(self.type)

class Scope:
    def __init__(self):
        self.locals = dict()

    def lookup(self, s):
        if s in self.locals.keys():
            return self.locals[s]
        return None

    def insert(self, s, t): #insert name s with type t.
        if s in self.locals.keys():
            print("Error. Name already in scope...")
            return
        self.locals[s] = SymbolEntry(t)

    def __str__(self):
        return "\n".join([f'{k} -> {v}' for k, v in self.locals.items()])

class SymbolTable:
    def __init__(self):
        self.scopes = []

    def openScope(self):
        self.scopes.append(Scope())

    def closeScope(self):
        self.scopes.pop()

    def insert(self, s, t):
        if len(self.scopes) == 0:
            self.scopes.append(Scope())
        sc = self.scopes[-1]
        sc.insert(s, t)

    def lookup(self, s):
        for sc in self.scopes[::-1]: # reverse
            name = sc.lookup(s)
            if name != None:
                return name

        return None

    def __str__(self):
        s = ''
        for index, sc in enumerate(self.scopes):
            s += f'\n-- Scope {index} --\n'
            s += f'{sc}\n'

        s += '----------------------\n'
        return s


# st = SymbolTable()
# st.openScope()
# st.insert("x", Type.INT)
# print(st)
# st.insert("y", Type.BOOL)
# print(f'x look up: {st.lookup("x")}')
# print(st)
# st.openScope()
# st.insert("x", Type.BOOL)
# print(st)
# print(f'x look up: {st.lookup("x")}')
# print(f'y look up: {st.lookup("y")}')
# st.closeScope()
# print(st)
# print(f'x look up: {st.lookup("x")}')
# st.closeScope()
# print(st)

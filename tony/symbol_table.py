from enum import Enum

class Type(Enum):
   INT = 1
   CHAR = 2
   BOOL = 3
   VOID = 4
   NIL = 5

class SymbolEntry:
    def __init__(self, type):
        self.type = type
    def __repr__(self):
        return self.type

class Scope:
    def __init__(self):
        self.locals = dict()

    def lookup(self, s):
        if s in self.locals.keys():
            return locals[s]
        return None

    def insert(self, s, t): #insert name s with type t.
        if s in self.locals.keys():
            print("Error. Name already in scope...")
            return
        self.locals[s] = SymbolEntry(t)
    def __repr__(self):
        return "\n".join([k + " " + str(v) for k, v in self.locals.items()])
    
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
        sc = self.scopes[len(self.scopes)-1]
        sc.insert(s, t)

    def lookup(self, s):
        for sc in self.scopes.reverse():
            name = sc.lookup(s)
            if name != None:
                return name
        return None

    def __repr__(self):
        s = ""
        for index, sc in enumerate(self.scopes):
            s += "-Scope " + str(index) + "-\n" + str(sc) + "\n"
        return s
            

st = SymbolTable()
st.openScope()
st.insert("x", "Type.INT")
print(st)
st.insert("y", "Type.BOOL")
print(st.lookup("x"))
print(st)
st.openScope()
st.insert("x", "Type.BOOL")
print(st.lookup("x"))
print(st.lookup("y"))
print(st)
st.closeScope()
print(st)
print(st.lookup("x"))
st.closeScope()
print(st)

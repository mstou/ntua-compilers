class SymbolEntry:
    ''' Abstract class for entries of the Symbol Table '''

class Variable(SymbolEntry):
    def __init__(self, name, type):
        self.type  = type
        self.name  = name

    def __str__(self):
        return f'Variable {self.name} of type {self.type}'

class FunctionParam(SymbolEntry):
    def __init__(self, name, type, reference=False):
        self.type = type
        self.name = name
        self.reference = reference

    def __str__(self):
        return f'Function parameter {self.name} of type'+\
               f'{"ref" if self.reference else ""} {self.type}'

class Function(SymbolEntry):
    def __init__(self, name, type, params):
        # params is an array of tuples: (name, type, reference)
        self.func_name   = name
        self.return_type = type
        self.params      = params
        self.defined     = False   # to distinguish functions that are declared
                                   # but not yet defined
    def __str__(self):
        s = f'{"Undefined" if not self.defined else ""} Function with:\n'
        s += f'\tFunction name: {self.func_name}\n'
        s += f'\tReturn type: {self.return_type}\n'
        s += f'\tParameters: ' + ' ,'.join(list(map(str, self.params)))
        return s

class Scope:
    def __init__(self):
        self.locals = dict()

    def lookup(self, s):
        if s in self.locals.keys():
            return self.locals[s]
        return None

    def insert(self, name, entry): #insert name s with type t.
        self.locals[name] = entry

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

    def lookup_current_scope(self, s):
        return self.scopes[-1].lookup(s)

    def __str__(self):
        s = ''
        for index, sc in enumerate(self.scopes):
            s += f'\n-- Scope {index} --\n'
            s += f'{sc}\n'

        s += '----------------------\n'
        return s


# st = SymbolTable()
# st.openScope()
# st.insert('x', Variable('x', BaseType.Int))
# print(st)
# st.insert('y', Variable('y',BaseType.Bool))
# print(f'x look up: {st.lookup("x")}')
# print(st)
# st.openScope()
# st.insert('x', Variable('x',BaseType.Bool))
# print(st)
# print(f'x look up: {st.lookup("x")}')
# print(f'y look up: {st.lookup("y")}')
# st.closeScope()
# print(st)
# print(f'x look up: {st.lookup("x")}')
# st.closeScope()
# print(st)

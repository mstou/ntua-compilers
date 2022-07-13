from .data_types import BaseType, Array

class SymbolEntry:
    ''' Abstract class for entries of the Symbol Table '''

class Variable(SymbolEntry):
    def __init__(self, name, type, cvalue=None):
        self.type  = type
        self.name  = name
        self.cvalue = cvalue

    def __str__(self):
        return f'Variable {self.name} of type {self.type}'

class FunctionParam(SymbolEntry):
    def __init__(self, name, type, reference=False, cvalue=None):
        self.type = type
        self.name = name
        self.reference = reference
        self.cvalue = cvalue

    def __str__(self):
        return f'Function parameter {self.name} of type'+\
               f'{"ref" if self.reference else ""} {self.type}'

class FunctionEntry(SymbolEntry):
    def __init__(self, name, type, params, defined=False, cvalue=None):
        # params is an array of tuples: (name, type, reference)
        self.func_name   = name
        self.return_type = type
        self.cavlue      = cvalue
        self.params      = params
        self.defined     = defined # to distinguish functions that are declared
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
    def __init__(self, skip_builtins=False):
        self.scopes = []

        if not skip_builtins:
            builtin_funcs = [
                ('puti', BaseType.Void, [('n', BaseType.Int, False)]),
                ('putb', BaseType.Void, [('b', BaseType.Bool, False)]),
                ('putc', BaseType.Void, [('c', BaseType.Char, False)]),
                ('puts', BaseType.Void, [('s', Array(BaseType.Char), False)]),
                ('geti', BaseType.Int, []),
                ('getb', BaseType.Bool, []),
                ('getc', BaseType.Char, []),
                ('gets', BaseType.Void, [('n', BaseType.Int, False), ('s', Array(BaseType.Char), False)]),
                ('abs', BaseType.Int, [('n', BaseType.Int, False)]),
                ('ord', BaseType.Int, [('c', BaseType.Char, False)]),
                ('chr', BaseType.Char, [('n', BaseType.Int, False)]),
                ('strlen', BaseType.Int, [('s', Array(BaseType.Char), False)]),
                ('strcmp', BaseType.Int, [('s1', Array(BaseType.Char), False),('s1', Array(BaseType.Char), False)]),
                ('strcpy', BaseType.Void, [('s1', Array(BaseType.Char), False),('s1', Array(BaseType.Char), False)]),
                ('strcat', BaseType.Void, [('s1', Array(BaseType.Char), False),('s1', Array(BaseType.Char), False)]),
            ]

            for f in builtin_funcs:
                self.insert(f[0], FunctionEntry(f[0],f[1],f[2]))


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

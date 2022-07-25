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
        self.cvalue      = cvalue
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
    def __init__(self, func_name=''):
        self.locals = dict()
        self.func_name = func_name
        self.returned  = False
        self.accesses_outside = set()

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
        self.id = 0

        self.builtins = [
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
        if not skip_builtins:
            for f in self.builtins:
                self.insert(f[0], FunctionEntry(f[0],f[1],f[2]))

    def openScope(self, name=''):
        self.scopes.append(Scope(name))

    def closeScope(self):
        if len(self.scopes) > 1:
            # we keep the accesses that were not from our scope
            # as we will have to pass them down

            for entry in self.scopes[-1].accesses_outside:
                if entry.name not in self.scopes[-2].locals:
                    self.scopes[-2].accesses_outside.add(entry)

        self.scopes.pop()

    def insert(self, s, t):
        if len(self.scopes) == 0:
            self.scopes.append(Scope())
        sc = self.scopes[-1]
        sc.insert(s, t)

    def lookup(self, s):
        local_scope = True # this is true for the first iteration

        for sc in self.scopes[::-1]: # reverse
            name = sc.lookup(s)

            if name != None:
                if not local_scope:
                    is_var = isinstance(name, Variable)
                    is_param = isinstance(name, FunctionParam)

                    if  is_var or is_param:
                        self.scopes[-1].accesses_outside.add(name)
                        # register the use of a global variable
                return name

            local_scope = False

        return None

    def register_return_statement(self):
        self.scopes[-1].returned = True

    def scope_has_returned(self):
        return self.scopes[-1].returned

    def get_scope_name(self):
        return self.scopes[-1].func_name

    def get_all_scope_names(self):
        return '_' + '_'.join([scope.func_name for scope in self.scopes])

    def get_global_accesses(self):
        return self.scopes[-1].accesses_outside

    def all_funcs_defined(self):
        ''' Checks if all functions that were declared
            in the last scope are also defined
        '''
        sc = self.scopes[-1].locals

        for name in sc:
            entry = sc[name]
            if isinstance(entry, FunctionEntry):
                if not entry.defined:
                    return False

        return True

    def lookup_current_scope(self, s):
        return self.scopes[-1].lookup(s)

    def __str__(self):
        s = ''
        for index, sc in enumerate(self.scopes):
            s += f'\n-- Scope {index} --\n'
            s += f'{sc}\n'

        s += '----------------------\n'
        return s

    def get_id(self):
        self.id += 1
        return self.id


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

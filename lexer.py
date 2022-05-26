import sys
import ply.lex as lex

# Declare the state
states = (
    ('multicomment','exclusive'),
)

# Key words
reserved = {
    'and' : 'AND',
    'bool': 'BOOL',
    'char': 'CHAR',
    'decl': 'DECL',
    'def' : 'DEF',
    'else': 'ELSE',
    'elsif': 'ELSIF',
    'end': 'END',
    'exit': 'EXIT',
    'false': 'FALSE',
    'for': 'FOR',
    'head': 'HEAD',
    'if': 'IF',
    'int': 'INT',
    'list': 'LIST',
    'mod': 'MOD',
    'new': 'NEW',
    r'nil\?': 'NIL2',
    'nil': 'NIL',
    'not': 'NOT',
    'or': 'OR',
    'ref': 'REF',
    'return': 'RETURN',
    'skip': 'SKIP',
    'tail': 'TAIL',
    'true': 'TRUE'
}

# List of token names.
tokens = [
    'NAME',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUAL',
    'NOTEQUAL',
    'LESS',
    'GREATER',
    'LEQ',
    'GEQ',
    'HASH',
    'LBRACKET',
    'RBRACKET',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'COLON',
    'SEMICOLON',
    'STRING',
    'ASSIGN',
] + list(reserved.values())

# Names
def t_NAME(t):
     r'[a-zA-Z_][a-zA-Z_0-9_\?]*'
     t.type = reserved.get(t.value, 'NAME') # Check for reserved words
     if (t.value == 'nil?'): t.type = 'NIL2'
     return t

# nil?
def t_NIL2(t):
    r'nil\?'
    return t

# Numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Symbolic operators
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_EQUAL    = r'='
t_NOTEQUAL = r'<>'
t_LESS     = r'<'
t_GREATER  = r'>'
t_LEQ      = r'<='
t_GEQ      = r'>='
t_HASH     = r'[#]'

# Seperators
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_COMMA     = r','
t_SEMICOLON = r';'
t_COLON     = r':'
t_ASSIGN    = r':='

# Char
t_CHAR = r'\'[^\'\"\\]\''

# Strings
t_STRING = r'\"[^\'\"\\]*\"'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_singlecomment(t):
     r'\%.*'
     pass
     # No return value. Token discarded

def t_multicomment(t):
    r'<\*'
    t.lexer.level = 1
    t.lexer.begin('multicomment')
    pass

def t_multicomment_open(t):
    r'<\*'
    t.lexer.level += 1
    pass

def t_multicomment_close(t):
    r'\*>'
    t.lexer.level -= 1
    if t.lexer.level == 0:
        t.lexer.begin('INITIAL')
    pass

def t_multicomment_symbols(t):
    r'.'
    pass

t_multicomment_ignore = ' \t\n'

def t_multicomment_error(t):
    print('Comment Error...')
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_error(t):
    print('Error...')
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex() # Use parameter debug=1 to debug

# input = '''
#         def hello ():
#           puts("Hello world!\n")
#         end
#         '''
# print(input)
# file = sys.argv[1]
# print(file)
#
# with open(file, 'r', encoding='unicode_escape') as f:
#     s = f.read()
#
# print(s)
# lexer.input(s)
#
# # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print((tok.type, tok.value))

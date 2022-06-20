import sys
import ply.yacc as yacc
from abstract_syntax_tree import Node

# Get the token map from the lexer.
from lexer import tokens

start = 'program'

precedence = (
     ('left', 'OR'),
     ('left', 'AND'),
     ('right', 'NOT'),
     ('nonassoc', 'EQUAL', 'NOTEQUAL', 'GREATER', 'LESS', 'GEQ', 'LEQ'),
     ('right', 'HASH'),
     ('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE', 'MOD'),
     ('right', 'UPLUS', 'UMINUS')
 )

def p_program(p):
    '''program : funcdef'''
    p[0] = Node('Program', 'program', [p[1]])

#======== Function definition ========
def p_funcdef(p):
    '''funcdef : DEF header COLON funcdefhelp stmt stmtlist END'''
    p[0] = Node('FuncDef', 'funcdef', [p[2], p[4], p[5], p[6]])

def p_funcdefhelp(p):
    '''funcdefhelp : funcdef funcdefhelp
                   | funcdecl funcdefhelp
                   | vardef funcdefhelp
                   | empty
                   '''
    if len(p) == 3:
        p[0] = Node('FuncDefHelp', 'funcdefhelp', [p[1], p[2]])
    elif len(p) == 2:
        p[0] = Node('FuncDefHelp', 'funcdefhelp', [p[1]])

#=========== Header ==============
def p_header(p):
    '''header : type NAME LPAREN formal formallist RPAREN
              | type NAME LPAREN RPAREN
              | NAME LPAREN formal formallist RPAREN
              | NAME LPAREN RPAREN
              '''
    if len(p) == 7:
        p[0] = Node('HeaderWithTypeArgs', 'headerWithTypeArgs' + p[2], [p[1], p[4], p[5]])
    elif len(p) == 5:
        p[0] = Node('HeaderWithTypeNoArgs', 'headerWithTypeNoArgs' + p[2], [p[1]])
    elif len(p) == 6:
        p[0] = Node('HeaderArgs', 'headerArgs' + p[1], [p[3], p[4]])
    elif len(p) == 4:
        p[0] = Node('HeaderNoArgs', 'headerNoArgs' + p[1])

#=========== Formal ==============
def p_formal(p):
    '''formal : REF vardef
              | vardef'''
    if len(p) == 3:
        p[0] = Node('RefFormal', 'refFormal', [p[2]])
    elif len(p) == 2:
        p[0] = Node('Formal', 'formal', [p[1]])

def p_formallist(p):
    '''formallist : SEMICOLON formal formallist
                  | empty
                  '''
    if len(p) == 4:
        p[0] = Node('FormalList', 'formallist', [p[2], p[3]])
    if len(p) == 2:
        p[0] = Node('FormalList', 'formallist', [p[1]])

# ================ Type ================
def p_type_simple(p):
    '''type : INT
            | BOOL
            | CHAR
            '''
    p[0] = Node('SimpleType', p[1])

def p_type_array(p):
    '''type : type LBRACKET RBRACKET'''
    p[0] = Node('ArrayType', '[]', [p[1]])

def p_type_list(p):
    '''type : LIST LBRACKET type RBRACKET'''
    p[0] = Node('ListType', 'list', [p[3]])

#=========== Func-decl ============
def p_funcdecl(p):
    '''funcdecl : DECL header'''
    p[0] = Node('FuncDecl', 'funcDecl', [p[2]])

#========== Var def ===============
def p_vardef(p):
    '''vardef : type name namelist'''
    p[0] = Node('VarDef', 'vardef', [p[1], p[2], p[3]])

def p_nameList(p):
    '''namelist : COMMA name namelist
                | empty
                '''
    if len(p) == 4:
        p[0] = Node('NameList', 'nameList', [p[2], p[3]])
    elif len(p) == 2:
        p[0] =  Node('NameList', 'nameList', [p[1]])

def p_name(p):
    '''name : NAME'''
    p[0] = Node('Name', p[1])

#=========== Statement ==================
def p_stmt_simple(p):
    '''stmt : simple'''
    p[0] = Node('Statement', 'stmt', [p[1]])

def p_stmt_exit(p):
    '''stmt : EXIT'''
    p[0] = Node('ExitStatement', 'exitStmt')

def p_stmt_return(p):
    '''stmt : RETURN expression'''
    p[0] = Node('ReturnStatement', 'returnStmt', [p[2]])

def p_stmt_if(p):
    '''stmt : if END'''
    p[0] = Node('IfStatement', 'ifStmt', [p[1]])

def p_stmt_if_elsif(p):
    '''stmt : if elsiflist END'''
    p[0] = Node('IfElsifStatement', 'ifElsifStmt', [p[1], p[2]])

def p_stmt_ifelse(p):
    '''stmt : if else END'''
    p[0] = Node('IfElseStatement', 'ifElseStmt', [p[1], p[2]])

def p_stmt_if_full(p):
    '''stmt : if elsiflist else END'''
    p[0] = Node('IfElsifElseStatement', 'ifElsifElseStmt', [p[1], p[2], p[3]])

def p_stmtlist(p):
    '''stmtlist : stmt stmtlist
                | empty
                '''
    if len(p) == 3:
        p[0] = Node('StmtList', 'stmtlist', [p[1], p[2]])
    elif len(p) == 2:
        p[0] = Node('StmtList', 'stmtlist', [p[1]])

def p_if(p):
    '''if : IF expression COLON stmt stmtlist'''
    p[0] = Node('If', 'if', [p[2], p[4], p[5]])

def p_elsif(p):
    '''elsif : ELSIF expression COLON stmt stmtlist'''
    p[0] = Node('ElsIf', 'elsIf', [p[2], p[4], p[5]])

def p_elsiflist(p):
    '''elsiflist : elsif elsiflist
                 | empty
                 '''
    if len(p) == 3:
        p[0] = Node('ElsIfList', 'elsIfList', [p[1], p[2]])
    elif len(p) == 2:
        p[0] = Node('ElsIfList', 'elsIfList', [p[1]])

def p_else(p):
    '''else : ELSE COLON stmt stmtlist'''
    p[0] = Node('Else', 'else', [p[3], p[4]])

def p_stmt_for(p):
    '''stmt : FOR simplelist SEMICOLON expression SEMICOLON simplelist COLON stmt stmtlist END'''
    p[0] = Node('ForStmt', 'for', [p[2], p[4], p[6], p[8], p[9]])

#=========== Simple ==============
def p_simple_skip(p):
    '''simple : SKIP'''
    p[0] = Node("SkipSimple", 'skip')

def p_simple_atomexpr(p):
    '''simple : atom ASSIGN expression'''
    p[0] = Node('AssignExpr', ':=', [p[1], p[3]])

def p_simple_call(p):
    '''simple : call'''
    p[0] = Node('CallSimple', 'simpleCall', [p[1]])

#======== Simple - List ===========
def p_simplelist(p):
    '''simplelist : simple simplelistcomma'''
    p[0] = Node('SimpleList', 'simpleList', [p[1], p[2]])

def p_simplelistcomma(p):
    '''simplelistcomma : COMMA simplelist
                       | empty
                       '''
    if len(p) == 3:
        p[0] = Node('SimpleListComma', 'simpleListComma', [p[2]])
    elif len(p) == 2:
        p[0] = Node('SimpleListComma', 'simpleListComma', [p[1]])


# #=========== Call ===============
def p_call(p):
    '''call : NAME LPAREN expression exprcomma RPAREN
            | NAME LPAREN expression RPAREN
            | NAME LPAREN RPAREN'''
    if len(p) == 6:
        p[0] = Node('Call', 'call ' + p[1], [p[3], p[4]])
    elif len(p) == 5:
        p[0] = Node('Call', 'call ' + p[1], [p[3]])
    elif len(p) == 4:
        p[0] = Node('Call', 'call ' + p[1])

#=========== Atom =================
def p_atom_id(p):
    '''atom : NAME'''
    p[0] = Node('IdAtom', p[1])

def p_atom_string(p):
    '''atom : STRING'''
    p[0] = Node('StrAtom', p[1])

def p_atom_expression(p):
    '''atom : atom LBRACKET expression RBRACKET'''
    p[0] = Node('ExprAtom', 'exprAtom', [p[1], p[3]])

def p_atom_call(p):
    '''atom : call'''
    p[0] = Node('CallAtom', 'callAtom', [p[1]])

#=========== Expression ================
def p_expression_atom(p):
    '''expression : atom'''
    p[0] = Node('AtomExpr', 'atomExpr', [p[1]])

def p_expression_int_const(p):
    '''expression : NUMBER'''
    p[0] = Node('int_cost', p[1])

def p_expression_char_const(p):
    '''expression : CHAR'''
    p[0] = Node('char_const', p[1])

def p_expression_parentheses(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = Node('ParenExpr', '()', [p[2]])

def p_expression_uminus(p):
     'expression : MINUS expression %prec UMINUS'
     p[0] = Node('UniArithmeticExpr', p[1], [p[2]])

def p_expression_uplus(p):
     'expression : PLUS expression %prec UPLUS'
     p[0] = Node('UniArithmeticExpr', p[1], [p[2]])

def p_expression_binary_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  '''
    p[0] = Node('BinArithmeticExpr', p[2], [p[1], p[3]])

def p_expression_compare(p):
    ''' expression : expression EQUAL expression
                   | expression NOTEQUAL expression
                   | expression LESS expression
                   | expression GREATER expression
                   | expression LEQ expression
                   | expression GEQ expression
                   '''
    p[0] = Node('CompExpr', p[2], [p[1], p[3]])

def p_expression_bool_const(p):
    '''expression : TRUE
                  | FALSE
                  '''
    p[0] = Node('bool_const', p[1])

def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = Node('NotExpr', 'not', [p[2]])

def p_expression_binary_boolean(p):
    '''expression : expression AND expression
                  | expression OR expression
                  '''
    p[0] = Node('BinBoolExpr', p[2], [p[1], p[3]])

def p_expression_new(p):
    '''expression : NEW type LBRACKET expression RBRACKET'''
    p[0] = Node('NewExpr', p[1], [p[2], p[4]])

def p_expression_nil(p):
    '''expression : NIL'''
    p[0] = Node('NilExpr', p[1])

def p_expression_nil2(p):
    '''expression : NIL2 LPAREN expression RPAREN'''
    p[0] = Node('Nil2Expr', p[1], [p[3]])

def p_expression_hash(p):
    '''expression : expression HASH expression'''
    p[0] = Node('HashExpr', p[2], [p[1], p[3]])

def p_expression_head(p):
    '''expression : HEAD LPAREN expression RPAREN'''
    p[0] = Node('HeadExpr', p[1], [p[3]])

def p_expression_tail(p):
    '''expression : TAIL LPAREN expression RPAREN'''
    p[0] = Node('TailExpr', 'tailExpr', [p[3]])

def p_exprcomma(p): # rule to parse: expr (, expr)*
    '''exprcomma : COMMA expression exprcomma
                 | empty
                 '''
    if len(p) == 4:
        p[0] = Node('CommaExpr', 'commaExpr', [p[2], p[3]])
    if len(p) == 2:
        p[0] = Node('CommaExpr', 'commaExpr', [p[1]])

#================= Empty =================
def p_empty(p):
    '''empty :'''
    p[0] = Node('Empty', 'empty')

#================= Error =================
def p_error(p):
    print('\x1b[0;30;41m' + 'Syntax error in input!' + '\x1b[0m')

# Build the parser
parser = yacc.yacc()

# file = sys.argv[1]
# print(file)
#
# with open(file, 'r', encoding='unicode_escape') as f:
#     s = f.read()
#     print(parser.parse(s, debug=0))

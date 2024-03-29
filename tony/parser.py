import sys
import ply.yacc as yacc
from .abstract_syntax_tree import *

# Get the token map from the lexer.
from .lexer import tokens

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
    p[0] = Program(p[1])

#======== Function definition ========
def p_funcdef(p):
    '''funcdef : DEF header COLON funcdefhelp stmt stmtlist END'''
    p[0] = FuncDef(p[2], p[4], p[5], p[6])

def p_funcdefhelp_funcdef(p):
    '''funcdefhelp : funcdef funcdefhelp'''
    p[0] = FuncDefHelp_FuncDef(p[1], p[2])

def p_funcdefhelp_funcdecl(p):
    '''funcdefhelp : funcdecl funcdefhelp'''
    p[0] = FuncDefHelp_FuncDecl(p[1], p[2])

def p_funcdefhelp_vardef(p):
    '''funcdefhelp : vardef funcdefhelp'''
    p[0] = FuncDefHelp_VarDef(p[1], p[2])

def p_funcdefhelp_empty(p):
    '''funcdefhelp : empty'''
    p[0] = FuncDefHelp(None, None)

#=========== Header ==============
def p_header(p):
    '''header : type NAME LPAREN formal formallist RPAREN
              | type NAME LPAREN RPAREN
              | NAME LPAREN formal formallist RPAREN
              | NAME LPAREN RPAREN
              '''
    if len(p) == 7:    # Rule 1
        p[0] = FunctionHeader(p[1], p[2], p[4], p[5])
    elif len(p) == 5:  # Rule 2
        p[0] = FunctionHeader(p[1], p[2], None, None)
    elif len(p) == 6:  # Rule 3
        p[0] = FunctionHeader(VoidNode(), p[1], p[3], p[4])
    elif len(p) == 4:  # Rule 4
        p[0] = FunctionHeader(VoidNode(), p[1], None, None)

#=========== Formal ==============
def p_formal(p):
    '''formal : REF vardef
              | vardef'''
    if len(p) == 3:
        p[0] = Formal(p[2], reference=True)
    elif len(p) == 2:
        p[0] = Formal(p[1], reference=False)

def p_formallist(p):
    '''formallist : SEMICOLON formal formallist
                  | empty
                  '''
    if len(p) == 4:
        p[0] = FormalList(p[2], p[3])
    elif len(p) == 2:
        p[0] = FormalList(None, None)

# ================ Type ================
def p_type_simple_int(p):
    '''type : INT'''
    p[0] = IntValue(p[1])

def p_type_simple_bool(p):
    '''type : BOOL'''
    p[0] = BooleanValue(p[1])

def p_type_simple_char(p):
    '''type : CHAR'''
    p[0] = CharValue(p[1])

def p_type_array(p):
    '''type : type LBRACKET RBRACKET'''
    p[0] = ArrayNode(p[1])

def p_type_list(p):
    '''type : LIST LBRACKET type RBRACKET'''
    p[0] = ListNode(p[3])

#=========== Func-decl ============
def p_funcdecl(p):
    '''funcdecl : DECL header'''
    p[0] = FuncDecl(p[2])

#========== Var def ===============
def p_vardef(p):
    '''vardef : type name namelist'''
    p[0] = VariableDefinition(p[1], names = [p[2]] + p[3].getNames())

def p_nameList(p):
    '''namelist : COMMA name namelist
                | empty
                '''
    if len(p) == 4:
        p[0] = NameList(p[2], p[3])
    elif len(p) == 2:
        p[0] =  NameList(None, None)

def p_name(p):
    '''name : NAME'''
    p[0] = p[1]

#=========== Statement ==================
def p_stmt_simple(p):
    '''stmt : simple'''
    p[0] = p[1]

def p_stmt_exit(p):
    '''stmt : EXIT'''
    p[0] = ExitStatement()

def p_stmt_return(p):
    '''stmt : RETURN expression'''
    p[0] = ReturnStatement(p[2])

def p_stmt_if(p):
    '''stmt : if END'''
    p[0] = p[1]

def p_stmt_if_elsif(p):
    '''stmt : if elsiflist END'''
    p[0] = IfElsifStatement(p[1], p[2])

def p_stmt_ifelse(p):
    '''stmt : if else END'''
    p[0] = IfElseStatement(p[1], p[2])

def p_stmt_if_full(p):
    '''stmt : if elsiflist else END'''
    p[0] = IfFullStatement(p[1], p[2], p[3])

def p_stmtlist(p):
    '''stmtlist : stmt stmtlist
                | empty
                '''
    if len(p) == 3:
        p[0] = StatementList(p[1], p[2])
    elif len(p) == 2:
        p[0] = StatementList(None, None)

def p_if(p):
    '''if : IF expression COLON stmt stmtlist'''
    p[0] = IfStatement(p[2], p[4], p[5])

def p_elsif(p):
    '''elsif : ELSIF expression COLON stmt stmtlist'''
    p[0] = ElsifStatement(p[2], p[4], p[5])

def p_elsiflist(p):
    '''elsiflist : elsif elsiflist
                 | empty
                 '''
    if len(p) == 3:
        p[0] = ElsifList(p[1], p[2])
    elif len(p) == 2:
        p[0] = ElsifList(None, None)

def p_else(p):
    '''else : ELSE COLON stmt stmtlist'''
    p[0] = ElseStatement(p[3], p[4])

def p_stmt_for(p):
    '''stmt : FOR simplelist SEMICOLON expression SEMICOLON simplelist COLON stmt stmtlist END'''
    p[0] = ForLoop(p[2], p[4], p[6], p[8], p[9])

#=========== Simple ==============
def p_simple_skip(p):
    '''simple : SKIP'''
    p[0] = SkipStatment()

def p_simple_atomexpr(p):
    '''simple : atom ASSIGN expression'''
    p[0] = Assignment(p[1], p[3])

def p_simple_call(p):
    '''simple : call'''
    p[0] = p[1]

#======== Simple - List ===========
def p_simplelist(p):
    '''simplelist : simple simplelistcomma'''
    p[0] = SimpleList(simples = [p[1]] + p[2].getSimples())

def p_simplelistcomma(p):
    '''simplelistcomma : COMMA simple simplelistcomma
                       | empty
                       '''
    if len(p) == 4:
        p[0] = SimpleListComma(p[2],p[3])
    elif len(p) == 2:
        p[0] = SimpleListComma(None,None)

# #=========== Call ===============
def p_call(p):
    '''call : NAME LPAREN expression exprcomma RPAREN
            | NAME LPAREN expression RPAREN
            | NAME LPAREN RPAREN'''
    if len(p) == 6:
        p[0] = FunctionCall(p[1], [p[3]] + p[4].getExpressions())
    elif len(p) == 5:
        p[0] = FunctionCall(p[1], [p[3]])
    elif len(p) == 4:
        p[0] = FunctionCall(p[1], [])

#=========== Atom =================
def p_atom_id(p):
    '''atom : NAME'''
    p[0] = VarAtom(p[1])

def p_atom_string(p):
    '''atom : STRING'''
    p[0] = StringAtom(p[1])

def p_atom_expression(p):
    '''atom : atom LBRACKET expression RBRACKET'''
    p[0] = AtomArray(p[1], p[3])

def p_atom_call(p):
    '''atom : call'''
    p[0] = p[1]

#=========== Expression ================
def p_expression_atom(p):
    '''expression : atom'''
    p[0] = p[1]

def p_expression_int_const(p):
    '''expression : NUMBER'''
    p[0] = IntValue(p[1])

def p_expression_char_const(p):
    '''expression : CHAR'''
    p[0] = CharValue(p[1])

def p_expression_parentheses(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = ParenthesisExpr(p[2])

def p_expression_uminus(p):
     'expression : MINUS expression %prec UMINUS'
     p[0] = UniArithmeticMINUS(p[2])

def p_expression_uplus(p):
     'expression : PLUS expression %prec UPLUS'
     p[0] = UniArithmeticPLUS(p[2])

def p_expression_binary_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  '''
    p[0] = BinaryOperator(p[1], p[2], p[3])

def p_expression_compare(p):
    ''' expression : expression EQUAL expression
                   | expression NOTEQUAL expression
                   | expression LESS expression
                   | expression GREATER expression
                   | expression LEQ expression
                   | expression GEQ expression
                   '''
    p[0] = BinaryComparison(p[1], p[2], p[3])


def p_expression_bool_const(p):
    '''expression : TRUE
                  | FALSE
                  '''
    p[0] = BooleanValue(p[1])

def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = Not(p[2])

def p_expression_binary_boolean(p):
    '''expression : expression AND expression
                  | expression OR expression
                  '''
    p[0] = BinaryBoolean(p[1], p[2], p[3])

def p_expression_new(p):
    '''expression : NEW type LBRACKET expression RBRACKET'''
    p[0] = NewArray(p[2], p[4])

def p_expression_nil(p):
    '''expression : NIL'''
    p[0] = EmptyListNode()

def p_expression_nil2(p):
    '''expression : NIL2 LPAREN expression RPAREN'''
    p[0] = isEmptyList(p[3])

def p_expression_hash(p):
    '''expression : expression HASH expression'''
    p[0] = ListOperator(p[1], p[3])

def p_expression_head(p):
    '''expression : HEAD LPAREN expression RPAREN'''
    p[0] = HeadOperator(p[3])

def p_expression_tail(p):
    '''expression : TAIL LPAREN expression RPAREN'''
    p[0] = TailOperator(p[3])

def p_exprcomma(p): # rule to parse: expr (, expr)*
    '''exprcomma : COMMA expression exprcomma
                 | empty
                 '''
    if len(p) == 4:
        p[0] = CommaExpr(p[2], p[3])
    if len(p) == 2:
        p[0] = CommaExpr(None, None)

#================= Empty =================
def p_empty(p):
    '''empty :'''
    p[0] = None

#================= Error =================
def p_error(p):
    errormsg = f'Syntax error in line {p.lineno}, unexpected token {p.value}'
    raise Exception(errormsg)

# Build the parser
parser = yacc.yacc()

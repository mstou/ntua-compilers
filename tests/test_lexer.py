import pytest
from context import lexer


def output(lexer, input):
    tokens = []
    # Give the lexer some input
    lexer.input(input)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        tokens.append((tok.type, tok.value))
    return tokens

@pytest.mark.lexer
def test_arithmetic():
    input = '''
        3 + 5-42 *7+ 8 / 2 +-*/
    '''
    tokens = output(lexer, input)
    expectedTokens = [
        ('NUMBER', 3),
        ('PLUS', '+'),
        ('NUMBER', 5),
        ('MINUS', '-'),
        ('NUMBER', 42),
        ('TIMES', '*'),
        ('NUMBER', 7),
        ('PLUS', '+'),
        ('NUMBER', 8),
        ('DIVIDE', '/'),
        ('NUMBER', 2),
        ('PLUS', '+'),
        ('MINUS', '-'),
        ('TIMES', '*'),
        ('DIVIDE', '/'),
    ]

    assert tokens == expectedTokens

@pytest.mark.lexer
def test_comparison():
    input = '''
        3 < 4 >=5 =42 <> 17 <<= >>= <> =
    '''
    tokens = output(lexer, input)
    expectedTokens = [
        ('NUMBER', 3),
        ('LESS', '<'),
        ('NUMBER', 4),
        ('GEQ', '>='),
        ('NUMBER', 5),
        ('EQUAL', '='),
        ('NUMBER', 42),
        ('NOTEQUAL', '<>'),
        ('NUMBER', 17),
        ('LESS', '<'),
        ('LEQ', '<='),
        ('GREATER', '>'),
        ('GEQ', '>='),
        ('NOTEQUAL', '<>'),
        ('EQUAL', '=')
    ]
    assert tokens == expectedTokens

@pytest.mark.lexer
def test_char():
    input = '''
        'a' '1' 'z' '\n' '\x1d'
    '''
    # what happens with backslash '\'?
    tokens = output(lexer, input)
    expectedTokens = [
        ('CHAR', "'a'"),
        ('CHAR', "'1'"),
        ('CHAR', "'z'"),
        ('CHAR', "'\n'"),
        ('CHAR', "'\x1d'"),

    ]
    assert tokens == expectedTokens

@pytest.mark.lexer
def test_string():
    input = '''
        "One must imagine"
        "Sisyphus happy."
        "-Albert Camus"
        "12345+*-/\t\n"
    '''
    tokens = output(lexer, input)
    expectedTokens = [
        ('STRING', '"One must imagine"'),
        ('STRING', '"Sisyphus happy."'),
        ('STRING', '"-Albert Camus"'),
        ('STRING', '"12345+*-/\t\n"')
    ]
    assert tokens == expectedTokens

@pytest.mark.lexer
def test_seperators():
    input = '''
        ()[];:,:=
    '''
    tokens = output(lexer, input)
    expectedTokens = [
        ('LPAREN', '('),
        ('RPAREN', ')'),
        ('LBRACKET', '['),
        ('RBRACKET', ']'),
        ('SEMICOLON', ';'),
        ('COLON', ':'),
        ('COMMA', ','),
        ('ASSIGN', ':=')
    ]
    assert tokens == expectedTokens

@pytest.mark.lexer
def test_keywords():
    input = '''
        nil?
        nil?ab
    '''
    tokens = output(lexer, input)
    expectedTokens = [
        ('NIL2', 'nil?'),
        ('NAME', 'nil?ab')
    ]
    assert tokens == expectedTokens

@pytest.mark.lexer
def test_names():
    input = '''
        variable x y
        xUpper yCamelCase
        Xlower aNum1234?
        y_Underscore_
    '''
    tokens = output(lexer, input)
    expectedTokens = [
        ('NAME', 'variable'),
        ('NAME', 'x'),
        ('NAME', 'y'),
        ('NAME', 'xUpper'),
        ('NAME', 'yCamelCase'),
        ('NAME', 'Xlower'),
        ('NAME', 'aNum1234?'),
        ('NAME', 'y_Underscore_')
    ]
    assert tokens == expectedTokens

@pytest.mark.lexer
def test_singleLineComments():
    input = '''
        % This is a comment
        % This is also a comment.!1234
    '''
    tokens = output(lexer, input)
    expectedTokens = []
    assert tokens == expectedTokens

@pytest.mark.lexer
def test_multipleLineComments():
    input = '''
        <* Comment *>
        <* This is a multi-
            line comment. *>
        <* This is a <* nested *> comment. *>
    '''
    tokens = output(lexer, input)
    expectedTokens = []
    assert tokens == expectedTokens

@pytest.mark.lexer
def test_mixed1():
    input = '''
        x = 1
        y = x + 42
        "String" % This is a comment
        if x < y
    '''
    tokens = output(lexer, input)
    expectedTokens = []
    pass

@pytest.mark.lexer
def test_HelloWorld():
    input = '''
        def hello ():
        puts("Hello world!\n")
        end
    '''
    tokens = output(lexer, input)
    expectedTokens = [
        ('DEF', 'def'),
        ('NAME', 'hello'),
        ('LPAREN', '('),
        ('RPAREN', ')'),
        ('COLON', ':'),
        ('NAME', 'puts'),
        ('LPAREN', '('),
        ('STRING', '\"Hello world!\n\"'),
        ('RPAREN', ')'),
        ('END', 'end')
    ]
    assert tokens == expectedTokens

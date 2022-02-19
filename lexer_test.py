from cmath import exp
import unittest
from lexer import lexer


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

class TestLexer(unittest.TestCase):

    def test_arithmetic(self):
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
        self.assertEqual(tokens, expectedTokens)

    def test_comparison(self):
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
        self.assertEqual(tokens, expectedTokens)

    def test_char(self):
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
        self.assertEqual(tokens, expectedTokens)
    
    def test_string(self):
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
        self.assertEqual(tokens, expectedTokens)

    def test_seperators(self):
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
        self.assertEqual(tokens, expectedTokens)

    def test_keywords(self):
        input = '''
            nil?
            nil?ab
        '''
        tokens = output(lexer, input)
        expectedTokens = [
            ('NIL2', 'nil?'),
            ('NAME', 'nil?ab')
        ]
        self.assertEqual(tokens, expectedTokens)

    def test_names(self):
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
        self.assertEqual(tokens, expectedTokens)
        
    def test_singleLineComments(self):
        input = '''
            % This is a comment
            % This is also a comment.!1234
        '''
        tokens = output(lexer, input)
        expectedTokens = []
        self.assertEqual(tokens, expectedTokens)
        
    def test_multipleLineComments(self):
        input = '''
            <* Comment *>
            <* This is a multi-
                line comment. *>
            <* This is a <* nested *> comment. *>
        '''
        tokens = output(lexer, input)
        expectedTokens = []
        self.assertEqual(tokens, expectedTokens)
        
    
    def test_mixed1(self):
        input = '''
            x = 1
            y = x + 42
            "String" % This is a comment
            if x < y
        '''
        tokens = output(lexer, input)
        expectedTokens = []
        pass
    
    def test_mixed2(self):
        pass
    
    def test_HelloWorld(self):
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
        self.assertEqual(tokens, expectedTokens)

# Run tests
unittest.main()

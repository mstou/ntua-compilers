test:
	pytest
	rm tony/parser.out
	rm tony/parsetab.py

lexer_test:
	pytest -v -m lexer
	rm tony/parser.out
	rm tony/parsetab.py
	
parser_test:
	pytest -v -m parser
	rm tony/parser.out
	rm tony/parsetab.py

CC = gcc
CFLAGS=-fPIC -shared -Wall -Werror

builtins: tony/builtins.c
	$(CC) tony/builtins.c -o libbuiltins.so $(CFLAGS)

clean:
	rm tony/parser.out
	rm tony/parsetab.py

test:
	pytest
	$(MAKE) clean

lexer_test:
	pytest -v -m lexer
	$(MAKE) clean

parser_test:
	pytest -v -m parser
	$(MAKE) clean

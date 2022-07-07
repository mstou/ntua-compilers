import pytest
from context import *

CORRECT_PREFIX = 'tony-programs/'

def readFile(file, prefix = CORRECT_PREFIX):
    with open(prefix + file, 'r', encoding = 'unicode_escape') as f:
        s = f.read()
    return s

@pytest.mark.semantics
def test_helloworld_semantics():
    input = readFile('helloworld.tony')

    s = SymbolTable()
    root = parser.parse(input).sem(s)

@pytest.mark.semantics
def test_bubblesort_semantics():
    input = readFile('bubblesort.tony')

    s = SymbolTable()
    root = parser.parse(input).sem(s)

@pytest.mark.semantics
def test_hanoi_semantics():
    input = readFile('hanoi.tony')

    s = SymbolTable()
    root = parser.parse(input).sem(s)

@pytest.mark.semantics
def test_primes_semantics():
    input = readFile('primes.tony')

    s = SymbolTable()
    root = parser.parse(input).sem(s)

@pytest.mark.semantics
def test_quicksort_semantics():
    input = readFile('quicksort.tony')

    s = SymbolTable()
    root = parser.parse(input).sem(s)

@pytest.mark.semantics
def test_string_reverse_semantics():
    input = readFile('string_reverse.tony')

    s = SymbolTable()
    root = parser.parse(input).sem(s)

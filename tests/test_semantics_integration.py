import pytest
from context import *

PROGRAMS_PREFIX = 'tony-programs/'
SEMANTICS_TESTS = PROGRAMS_PREFIX + 'incorrect-semantics/'

def readFile(file, prefix = PROGRAMS_PREFIX):
    with open(prefix + file, 'r', encoding = 'unicode_escape') as f:
        s = f.read()
    return s

@pytest.mark.semantics
def test_array_invalid_index():
    input = readFile('array_invalid_index.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)

@pytest.mark.semantics
def test_array_invalid_value():
    input = readFile('array_invalid_value.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)

@pytest.mark.semantics
def test_list_incorrect_initialization():
    input = readFile('list_incorrect_initialization.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)
        
@pytest.mark.semantics
def test_list_multiple_types():
    input = readFile('list_multiple_types.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)


@pytest.mark.semantics
def test_incorrect_program_w_params():
    input = readFile('program_w_params.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)

@pytest.mark.semantics
def test_incorrect_program_w_return_type():
    input = readFile('program_w_return_type.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)

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

@pytest.mark.semantics
def test_lval_fun_semantics():
    input = readFile('lval_fun.tony')

    s = SymbolTable()
    root = parser.parse(input).sem(s)

@pytest.mark.semantics
def test_var_shadowing_extreme_semantics():
    input = readFile('var_shadowing_extreme.tony')

    s = SymbolTable()
    root = parser.parse(input).sem(s)

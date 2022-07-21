import pytest
from context import *

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
def test_function_call_extra_args():
    input = readFile('function_call_extra_args.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)

@pytest.mark.semantics
def test_function_call_wrong_args():
    input = readFile('function_call_wrong_args.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)

@pytest.mark.semantics
def test_function_call_extra_args2():
    input = readFile('function_call_wrong_args2.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)

@pytest.mark.semantics
def test_function_call_wrong_type():
    input = readFile('function_call_wrong_type.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)

@pytest.mark.semantics
def test_function_declared_not_defined():
    input = readFile('function_declared_not_defined.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)

@pytest.mark.semantics
def test_function_missing_return():
    input = readFile('function_missing_return.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)

@pytest.mark.semantics
def test_function_mutual_recursion():
    input = readFile('function_mutual_recursion.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)

@pytest.mark.semantics
def test_function_void_return():
    input = readFile('function_void_return.tony', prefix = SEMANTICS_TESTS)
    s = SymbolTable()
    root = parser.parse(input)

    assert root != None

    with pytest.raises(Exception):
        root.sem(s)

@pytest.mark.semantics
def test_function_wrong_ret_type():
    input = readFile('function_wrong_ret_type.tony', prefix = SEMANTICS_TESTS)
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
def test_function_call_semantics():
    input = readFile('function_call.tony')

    s = SymbolTable()
    root = parser.parse(input).sem(s)

@pytest.mark.semantics
def test_function_mutual_recursion():
    input = readFile('function_mutual_recursion.tony')

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

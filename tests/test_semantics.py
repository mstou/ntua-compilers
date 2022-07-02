import pytest
from context import *

@pytest.mark.semantics
def test_simple_arithmetic_expression():
    ''' expr: 1 + 42 * 17 / 73 - 8 '''

    a1 = BinaryOperator(IntValue(42), '*', IntValue(17))
    a2 = BinaryOperator(a1, '/', IntValue(73))
    a3 = BinaryOperator(IntValue(1), '+', a2)
    a4 = BinaryOperator(a3, '-', IntValue(8))

    assert a4.sem(SymbolTable()) == BaseType.Int

@pytest.mark.semantics
def test_simple_logical_expression():
    ''' expr: true and false or true and false '''

    a1 = BinaryBoolean(BooleanValue('true'), 'and', BooleanValue('false'))
    a2 = BinaryBoolean(a1, 'or', BooleanValue('true'))
    a3 = BinaryBoolean(a2, 'and', BooleanValue('false'))

    assert a3.sem(SymbolTable()) == BaseType.Bool

@pytest.mark.semantics
def test_simple_comparison_expression():
    ''' expr: (8 % 3 + 1) < 73 '''

    a1 = BinaryOperator(IntValue(8), 'mod', IntValue(3))
    a2 = BinaryOperator(a1, '+', IntValue(1))
    a3 = BinaryComparison(a2, '<', IntValue(73))

    assert a3.sem(SymbolTable()) == BaseType.Bool

@pytest.mark.semantics
def test_equality_expressions():
    i1 = IntValue(73)
    i2 = IntValue(42)

    c1 = CharValue('a')
    c2 = CharValue('b')

    b1 = BooleanValue(False)
    b2 = BooleanValue(True)

    assert BinaryComparison(i1, '=', i2).sem(SymbolTable()) == BaseType.Bool
    assert BinaryComparison(c1, '=', c2).sem(SymbolTable()) == BaseType.Bool
    assert BinaryComparison(b1, '=', b2).sem(SymbolTable()) == BaseType.Bool

    with pytest.raises(Exception):
        BinaryComparison(i1, '=', c1).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(i1, '=', b1).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(b1, '=', c1).sem(SymbolTable())

@pytest.mark.semantics
def test_inequality_expressions():
    i1 = IntValue(73)
    i2 = IntValue(42)

    c1 = CharValue('a')
    c2 = CharValue('b')

    b1 = BooleanValue(False)
    b2 = BooleanValue(True)

    assert BinaryComparison(i1, '<>', i2).sem(SymbolTable()) == BaseType.Bool
    assert BinaryComparison(c1, '<>', c2).sem(SymbolTable()) == BaseType.Bool
    assert BinaryComparison(b1, '<>', b2).sem(SymbolTable()) == BaseType.Bool

    with pytest.raises(Exception):
        BinaryComparison(i1, '<>', c1).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(i1, '<>', b1).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(b1, '<>', c1).sem(SymbolTable())

@pytest.mark.semantics
def test_less_that_expressions():
    i1 = IntValue(73)
    i2 = IntValue(42)

    c1 = CharValue('a')
    c2 = CharValue('b')

    b1 = BooleanValue(False)
    b2 = BooleanValue(True)

    assert BinaryComparison(i1, '<', i2).sem(SymbolTable()) == BaseType.Bool
    assert BinaryComparison(c1, '<', c2).sem(SymbolTable()) == BaseType.Bool

    with pytest.raises(Exception):
        BinaryComparison(i1, '<', c1).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(i1, '<', b1).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(b1, '<', c1).sem(SymbolTable())


@pytest.mark.semantics
def test_leq_expressions():
    i1 = IntValue(73)
    i2 = IntValue(42)

    c1 = CharValue('a')
    c2 = CharValue('b')

    b1 = BooleanValue(False)
    b2 = BooleanValue(True)

    assert BinaryComparison(i1, '<=', i2).sem(SymbolTable()) == BaseType.Bool
    assert BinaryComparison(c1, '<=', c2).sem(SymbolTable()) == BaseType.Bool

    with pytest.raises(Exception):
        BinaryComparison(i1, '<=', c1).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(i1, '<=', b1).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(b1, '<=', c1).sem(SymbolTable())


@pytest.mark.semantics
def test_greater_than_expressions():
    i1 = IntValue(73)
    i2 = IntValue(42)

    c1 = CharValue('a')
    c2 = CharValue('b')

    b1 = BooleanValue(False)
    b2 = BooleanValue(True)

    assert BinaryComparison(i1, '>', i2).sem(SymbolTable()) == BaseType.Bool
    assert BinaryComparison(c1, '>', c2).sem(SymbolTable()) == BaseType.Bool

    with pytest.raises(Exception):
        BinaryComparison(i1, '>', c1).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(i1, '>', b1).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(b1, '>', c1).sem(SymbolTable())

@pytest.mark.semantics
def test_geq_expressions():
    i1 = IntValue(73)
    i2 = IntValue(42)

    c1 = CharValue('a')
    c2 = CharValue('b')

    b1 = BooleanValue(False)
    b2 = BooleanValue(True)

    assert BinaryComparison(i1, '>=', i2).sem(SymbolTable()) == BaseType.Bool
    assert BinaryComparison(c1, '>=', c2).sem(SymbolTable()) == BaseType.Bool

    with pytest.raises(Exception):
        BinaryComparison(i1, '>=', c1).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(i1, '>=', b1).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(b1, '>=', c1).sem(SymbolTable())

@pytest.mark.semantics
def test_arithmetic_expr_undefined_var():
    i = IntValue(73)
    x = VarAtom('x')

    with pytest.raises(Exception):
        BinaryOperator(i, '+', x).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryOperator(i, '-', x).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryOperator(i, '*', x).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryOperator(i, '/', x).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryOperator(i, 'mod', x).sem(SymbolTable())

@pytest.mark.semantics
def test_logic_expr_undefined_var():
    b = BooleanValue(True)
    x = VarAtom('x')

    with pytest.raises(Exception):
        BinaryBoolean(b, 'and', x).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryBoolean(b, 'or', x).sem(SymbolTable())

@pytest.mark.semantics
def test_comparison_expr_undefined_var():
    i = IntValue(73)
    x = VarAtom('x')

    with pytest.raises(Exception):
        BinaryComparison(i, '<', x).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(i, '>', x).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(i, '<=', x).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(i, '>=', x).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(i, '=', x).sem(SymbolTable())

    with pytest.raises(Exception):
        BinaryComparison(i, '<>', x).sem(SymbolTable())

@pytest.mark.semantics
def test_arithmetic_expr_defined_var_wrong_type():
    i = IntValue(73)
    x = VarAtom('x')
    s = SymbolTable()
    s.insert('x', BaseType.Bool)

    with pytest.raises(Exception):
        BinaryOperator(i, '+', x).sem(s)

    with pytest.raises(Exception):
        BinaryOperator(i, '-', x).sem(s)

    with pytest.raises(Exception):
        BinaryOperator(i, '*', x).sem(s)

    with pytest.raises(Exception):
        BinaryOperator(i, '/', x).sem(s)

    with pytest.raises(Exception):
        BinaryOperator(i, 'mod', x).sem(s)

@pytest.mark.semantics
def test_logic_expr_defined_var_wrong_type():
    b = BooleanValue(True)
    x = VarAtom('x')
    s = SymbolTable()
    s.insert('x', BaseType.Char)

    with pytest.raises(Exception):
        BinaryBoolean(b, 'and', x).sem(s)

    with pytest.raises(Exception):
        BinaryBoolean(b, 'or', x).sem(s)

@pytest.mark.semantics
def test_comparison_expr_defined_var_wrong_type():
    i = IntValue(73)
    x = VarAtom('x')
    s = SymbolTable()
    s.insert('x', BaseType.Bool)

    with pytest.raises(Exception):
        BinaryComparison(i, '<', x).sem(s)

    with pytest.raises(Exception):
        BinaryComparison(i, '>', x).sem(s)

    with pytest.raises(Exception):
        BinaryComparison(i, '<=', x).sem(s)

    with pytest.raises(Exception):
        BinaryComparison(i, '>=', x).sem(s)

    with pytest.raises(Exception):
        BinaryComparison(i, '=', x).sem(s)

    with pytest.raises(Exception):
        BinaryComparison(i, '<>', x).sem(s)

@pytest.mark.semantics
def test_arithmetic_expr_defined_var_correct_type():
    i = IntValue(73)
    x = VarAtom('x')
    s = SymbolTable()
    s.insert('x', BaseType.Int)

    assert BinaryOperator(i, '+', x).sem(s)   == BaseType.Int
    assert BinaryOperator(i, '-', x).sem(s)   == BaseType.Int
    assert BinaryOperator(i, '*', x).sem(s)   == BaseType.Int
    assert BinaryOperator(i, '/', x).sem(s)   == BaseType.Int
    assert BinaryOperator(i, 'mod', x).sem(s) == BaseType.Int

@pytest.mark.semantics
def test_logic_expr_defined_var_correct_type():
    b = BooleanValue(True)
    x = VarAtom('x')
    s = SymbolTable()
    s.insert('x', BaseType.Bool)

    assert BinaryBoolean(b, 'and', x).sem(s) == BaseType.Bool
    assert BinaryBoolean(b, 'or', x).sem(s)  == BaseType.Bool

@pytest.mark.semantics
def test_comparison_expr_defined_var_correct_type():
    i = IntValue(73)
    x = VarAtom('x')
    s = SymbolTable()
    s.insert('x', BaseType.Int)

    assert BinaryComparison(i, '<', x).sem(s)  == BaseType.Bool
    assert BinaryComparison(i, '>', x).sem(s)  == BaseType.Bool
    assert BinaryComparison(i, '<=', x).sem(s) == BaseType.Bool
    assert BinaryComparison(i, '>=', x).sem(s) == BaseType.Bool
    assert BinaryComparison(i, '=', x).sem(s)  == BaseType.Bool
    assert BinaryComparison(i, '<>', x).sem(s) == BaseType.Bool

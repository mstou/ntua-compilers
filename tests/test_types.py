import pytest
from context import (
    Type,
    BaseType,
    CompositeType,
    List,
    Array,
    Function
)


@pytest.mark.types
def test_basic_types_equality():
    i1 = BaseType.Int
    i2 = BaseType.Int

    c1 = BaseType.Char
    c2 = BaseType.Char

    b1 = BaseType.Bool
    b2 = BaseType.Bool

    e1 = BaseType.Nil
    e2 = BaseType.Nil

    v = BaseType.Void

    assert i1 == i2
    assert c1 == c2
    assert e1 == e2
    assert i1 != c1
    assert i1 != b1
    assert i1 != e1
    assert i1 != v
    assert c1 != v
    assert b1 != v
    assert e1 != v

@pytest.mark.types
def test_list_equality():
    l1 = List(BaseType.Int)
    l2 = List(BaseType.Int)
    l3 = List(List(Array(List(BaseType.Char))))
    l4 = List(List(Array(List(BaseType.Char))))
    l5 = List(List(BaseType.Bool))
    l6 = List(List(BaseType.Bool))

    assert l1 == l2
    assert l3 == l4
    assert l5 == l6
    assert l1 != l3
    assert l1 != l5
    assert l3 != l5

@pytest.mark.types
def test_array_equality():
    a1 = Array(BaseType.Int)
    a2 = Array(BaseType.Int)
    a3 = Array(Array(List(BaseType.Bool)))
    a4 = Array(Array(List(BaseType.Bool)))
    a5 = Array(Array(BaseType.Char))
    a6 = Array(Array(BaseType.Char))

    assert a1 == a2
    assert a3 == a4
    assert a5 == a6
    assert a1 != a3
    assert a1 != a5
    assert a3 != a5

import pytest

@pytest.mark.lexer
def test_silly():
    assert True

@pytest.mark.lexer
def test_best_num():
    best_num = 73
    assert (best_num == 73)

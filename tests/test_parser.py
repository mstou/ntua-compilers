import pytest
from context import parser, readFile

@pytest.mark.parser
def test_bubblesort():
    input = readFile('bubblesort.tony')

    assert parser.parse(input) != None

@pytest.mark.parser
def test_hanoi():
    input = readFile('hanoi.tony')

    assert parser.parse(input) != None

@pytest.mark.parser
def test_helloworld():
    input = readFile('helloworld.tony')

    assert parser.parse(input) != None

@pytest.mark.parser
def test_primes():
    input = readFile('primes.tony')

    assert parser.parse(input) != None

@pytest.mark.parser
def test_quicksort():
    input = readFile('quicksort.tony')

    assert parser.parse(input) != None

@pytest.mark.parser
def test_string_reverse():
    input = readFile('string_reverse.tony')

    assert parser.parse(input) != None

@pytest.mark.parser
def test_random_input():

    with pytest.raises(Exception):
        parser.parse('lol')

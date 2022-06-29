import pytest
from context import parser

PATH_PREFIX = 'tony-programs/'

def readFile(file):
    with open(PATH_PREFIX + file, 'r', encoding = 'unicode_escape') as f:
        s = f.read()
    return s

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
    assert parser.parse('lol') == None

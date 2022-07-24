import os
import pytest
import subprocess
from context import compile, CORRECT_PROGRAMS, TEST_INPUTS


@pytest.mark.end2end
def test_hello_world():
    compile(CORRECT_PROGRAMS + 'helloworld.tony')

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'helloworld/output_1.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_primes():
    compile(CORRECT_PROGRAMS + 'primes.tony')

    for i in range(1,4):
        output_file = TEST_INPUTS + f'primes/output_{i}.txt'
        input_file  = TEST_INPUTS + f'primes/input_{i}.txt'

        result = subprocess.run(f'./a.out < {input_file}', shell=True, stdout=subprocess.PIPE)

        with open(output_file, 'r') as f:
            expected_output = f.read()

        assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_string_reverse():
    compile(CORRECT_PROGRAMS + 'string_reverse.tony')

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'string_reverse/output_1.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_is_palindrome():
    compile(CORRECT_PROGRAMS + 'is_palindrome.tony')

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'is_palindrome/output.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_array_addition():
    compile(CORRECT_PROGRAMS + 'array_addition.tony')

    for i in range(1,3):
        output_file = TEST_INPUTS + f'array_addition/output_{i}.txt'
        input_file  = TEST_INPUTS + f'array_addition/input_{i}.txt'

        result = subprocess.run(f'./a.out < {input_file}', shell=True, stdout=subprocess.PIPE)

        with open(output_file, 'r') as f:
            expected_output = f.read()

        assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

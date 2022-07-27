import os
import pytest
import subprocess
from context import compile, CORRECT_PROGRAMS, TEST_INPUTS

@pytest.mark.end2end
def test_array_addition():
    compile(CORRECT_PROGRAMS + 'array_addition.tony', testing=True)

    for i in range(1,3):
        output_file = TEST_INPUTS + f'array_addition/output_{i}.txt'
        input_file  = TEST_INPUTS + f'array_addition/input_{i}.txt'

        result = subprocess.run(f'./a.out < {input_file}', shell=True, stdout=subprocess.PIPE)

        with open(output_file, 'r') as f:
            expected_output = f.read()

        assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_array_addition_2d():
    compile(CORRECT_PROGRAMS + 'array_addition_2d.tony', testing=True)

    for i in range(1,4):
        output_file = TEST_INPUTS + f'array_addition_2d/output_{i}.txt'
        input_file  = TEST_INPUTS + f'array_addition_2d/input_{i}.txt'

        result = subprocess.run(f'./a.out < {input_file}', shell=True, stdout=subprocess.PIPE)

        with open(output_file, 'r') as f:
            expected_output = f.read()

        assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_array_io():
    compile(CORRECT_PROGRAMS + 'array_io.tony', testing=True)

    for i in range(1,3):
        output_file = TEST_INPUTS + f'array_io/output_{i}.txt'
        input_file  = TEST_INPUTS + f'array_io/input_{i}.txt'

        result = subprocess.run(f'./a.out < {input_file}', shell=True, stdout=subprocess.PIPE)

        with open(output_file, 'r') as f:
            expected_output = f.read()

        assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_bubblesort():
    compile(CORRECT_PROGRAMS + 'bubblesort.tony', testing=True)

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'bubblesort/output_1.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_dfs():
    compile(CORRECT_PROGRAMS + 'dfs.tony', testing=True)

    for i in range(1,5):
        output_file = TEST_INPUTS + f'dfs/output_{i}.txt'
        input_file  = TEST_INPUTS + f'dfs/input_{i}.txt'

        result = subprocess.run(f'./a.out < {input_file}', shell=True, stdout=subprocess.PIPE)

        with open(output_file, 'r') as f:
            expected_output = f.read()

        assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_exit_void():
    compile(CORRECT_PROGRAMS + 'exit_void.tony', testing=True)

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'exit_void/output_1.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_function_call():
    compile(CORRECT_PROGRAMS + 'function_call.tony', testing=True)

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'function_call/output_1.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_function_mutual_recursion():
    compile(CORRECT_PROGRAMS + 'function_mutual_recursion.tony', testing=True)

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'function_mutual_recursion/output_1.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')


@pytest.mark.end2end
def test_function_pass_by_ref():
    compile(CORRECT_PROGRAMS + 'function_pass_by_ref.tony', testing=True)

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'function_pass_by_ref/output_1.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_hello_world():
    compile(CORRECT_PROGRAMS + 'helloworld.tony', testing=True)

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'helloworld/output_1.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_is_palindrome():
    compile(CORRECT_PROGRAMS + 'is_palindrome.tony', testing=True)

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'is_palindrome/output.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_primes():
    compile(CORRECT_PROGRAMS + 'primes.tony', testing=True)

    for i in range(1,4):
        output_file = TEST_INPUTS + f'primes/output_{i}.txt'
        input_file  = TEST_INPUTS + f'primes/input_{i}.txt'

        result = subprocess.run(f'./a.out < {input_file}', shell=True, stdout=subprocess.PIPE)

        with open(output_file, 'r') as f:
            expected_output = f.read()

        assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_quicksort():
    compile(CORRECT_PROGRAMS + 'quicksort.tony', testing=True)

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'quicksort/output_1.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_scopes():
    compile(CORRECT_PROGRAMS + 'scopes.tony', testing=True)

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'scopes/output_1.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

@pytest.mark.end2end
def test_string_reverse():
    compile(CORRECT_PROGRAMS + 'string_reverse.tony', testing=True)

    result = subprocess.run('./a.out', shell=True, stdout=subprocess.PIPE)
    output_file = TEST_INPUTS + 'string_reverse/output_1.txt'
    expected_output = ''

    with open(output_file, 'r') as f:
        expected_output = f.read()

    assert result.stdout.decode("utf-8") == expected_output

    os.remove('a.out')

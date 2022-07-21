import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tony  import *
from tonyc import compile

TEST_INPUTS = 'tests/test-inputs/'
PROGRAMS_PREFIX  = 'tony-programs/'
SEMANTICS_TESTS  = PROGRAMS_PREFIX + 'incorrect-semantics/'
CORRECT_PROGRAMS = PROGRAMS_PREFIX + 'correct-programs/'

def readFile(file, prefix = CORRECT_PROGRAMS):
    with open(prefix + file, 'r', encoding = 'unicode_escape') as f:
        s = f.read()
    return s

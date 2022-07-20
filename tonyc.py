#!/usr/bin/env python3

import os
import argparse
from tony import *

BUILTINS_LIB = 'libbuiltins.so'
LLVM_OUTPUT  = 'a.ll'
AS_OUTPUT    = 'a.s'
EXECUTABLE   = 'a.out'

def readFile(file):
    with open(file, 'r', encoding = 'unicode_escape') as f:
        s = f.read()
    return s

argparser = argparse.ArgumentParser()
argparser.add_argument('filename', default='', type=str)
args = argparser.parse_args()

if BUILTINS_LIB not in os.listdir():
    os.system('make builtins')

file = args.filename
code = readFile(file)
ast = parser.parse(code)
ast.sem(SymbolTable())
with open(LLVM_OUTPUT, 'w') as f:
    print(ast.codegen(), file = f)

os.system(f'llc {LLVM_OUTPUT} --relocation-model=pic -o {AS_OUTPUT}')
os.system(f'gcc {AS_OUTPUT} -L . -lbuiltins -o {EXECUTABLE}')
os.system(f'export LD_LIBRARY_PATH={os.getcwd()}')
os.remove(LLVM_OUTPUT)
os.remove(AS_OUTPUT)

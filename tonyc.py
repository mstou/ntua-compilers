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

def compile(file,
            llvm_output=LLVM_OUTPUT,
            as_output=AS_OUTPUT,
            executable=EXECUTABLE,
            show_commands=False):

    if BUILTINS_LIB not in os.listdir():
        cmd_make_builtins = '$(make) builtins'
        os.system(cmd_make_builtins)

        if show_commands: print(cmd_make_builtins)

    code = readFile(file)
    ast = parser.parse(code)
    ast.sem(SymbolTable())
    with open(LLVM_OUTPUT, 'w') as f:
        print(ast.codegen(), file = f)

    cmd_llc = f'llc {llvm_output} --relocation-model=pic -o {as_output}'
    os.system(cmd_llc)
    if show_commands: print(cmd_llc)

    cmd_gcc = f'gcc {as_output} -L . -Wl,-rpath={os.getcwd()} -lbuiltins -o {executable}'
    os.system(cmd_gcc)
    if show_commands: print(cmd_gcc)

    os.remove(llvm_output)
    if show_commands: print(f'rm {llvm_output}')

    os.remove(as_output)
    if show_commands: print(f'rm {as_output}')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('filename', default='', type=str)
    args = argparser.parse_args()

    compile(args.filename, show_commands=False)

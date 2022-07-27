#!/usr/bin/env python3

import os
import argparse
from tony import *

BUILTINS_LIB = 'libbuiltins.so'


def readFile(file):
    with open(file, 'r', encoding = 'unicode_escape') as f:
        s = f.read()
    return s

def compile(file,
            llvm_to_stdout=False,
            as_to_stdout=False,
            only_ast=False,
            show_commands=True,
            optimization=1,
            testing=False):

    if BUILTINS_LIB not in os.listdir():
        cmd_make_builtins = '$(make) builtins'
        os.system(cmd_make_builtins)

        if show_commands: print(cmd_make_builtins)

    ''' Reading the code '''
    if file == None:
        testing = True
        sys.stdin.reconfigure(encoding='unicode_escape')
        code = sys.stdin.read()
    else:
        file_prefix = file.split('.')[0]
        code = readFile(file)

    ''' Lexing & Parsing '''
    try:
        ast = parser.parse(code)

    except Exception as e:
        print(e)
        exit()

    ''' Printing the Abstract Syntax Tree '''
    if only_ast:
        print(ast)
        exit()

    try:
        ast.sem(SymbolTable())

    except Exception as e:
        print(e)
        exit()

    ''' LLVM IR Code Generation '''
    # llvm_ir = str(ast.codegen(opt_level=0))

    if llvm_to_stdout:
        print(llvm_ir)
    else:
        llvm_output = 'a.ll' if testing else f'{file_prefix}.ll'

        with open(llvm_output, 'w') as f:
            print(ast.codegen(), file=f)

    ''' Compiling to Assembly '''
    as_output = 'a.s' if testing else f'{file_prefix}.s'

    cmd_llc = f'llc {llvm_output} --relocation-model=pic -o {as_output}'
    os.system(cmd_llc)
    if show_commands: print(cmd_llc)

    if as_to_stdout:
        with open(as_output, r) as f:
            print(f.read())

    ''' Making the final executable '''
    executable = 'a.out' if testing else f'{file_prefix}.out'
    cmd_gcc = f'gcc {as_output} -L . -Wl,-rpath={os.getcwd()} -lbuiltins -o {executable}'
    os.system(cmd_gcc)
    if show_commands: print(cmd_gcc)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('filename', default='', type=str, nargs='?')
    argparser.add_argument('-f', action='store_true')
    argparser.add_argument('-i', action='store_true')
    argparser.add_argument('-O2', action='store_true')
    argparser.add_argument('-O3', action='store_true')
    argparser.add_argument('-commands', action='store_true')

    args = argparser.parse_args()

    optimization = 1
    if args.O2:
        optimization = 2
    if args.O3:
        optimization = 3

    if args.f or args.i:
        file = None
    else:
        file = args.filename

    compile(file, show_commands=args.commands, optimization=optimization)

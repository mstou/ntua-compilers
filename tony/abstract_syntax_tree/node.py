from .data_types   import BaseType
from .symbol_table import SymbolTable, FunctionEntry
from .llvm_types   import BaseType_to_LLVM, LLVM_Types

from llvmlite import ir, binding

class Node:
    def __init__(self, type, value, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []

    def sem(self, symbol_table):
        '''
            Semantic Analysis

            1) Checks that all children are semantically correct
            2) Makes the necessary changes to the symbol table
            3) Returns its type
        '''
        pass

    def codegen(self, module, builder, symbol_table):
        '''
            LLVM Code generation

            Adds the necessary instructions to the IR Builder
            and returns an LLVM Value (where applicable)
        '''
        pass

    def pprint(self, indent=0):
        return indentation(indent) +\
               f'Instance of {self.__class__.__name__}'

    def __str__(self):
        return self.pprint()


class Program(Node):
    def __init__(self, funcdef):
        self.main = funcdef
        self.symbol_table = None # will be initialized when sem is called
        self.module  = None
        self.binding = None
        self.builder = None
        self.c_symbol_table = SymbolTable(skip_builtins=True)

    def codegen_init(self):
        ''' Initializes  llvm '''
        self.binding = binding
        self.binding.initialize()
        self.binding.initialize_native_target()
        self.binding.initialize_native_asmprinter()

        self.module = ir.Module()
        self.module.triple = self.binding.get_default_triple()
        self.target_data = self.binding.Target.from_default_triple().create_target_machine().target_data
        self.c_symbol_table.setTargetData(self.target_data)

        self.builder = None # the builder will be declared inside the function definition

        for f in self.c_symbol_table.builtins:
            name, type, args = f
            arg_types_llvm = list(map(lambda arg: BaseType_to_LLVM(arg[1]), args))
            ftype = ir.FunctionType(BaseType_to_LLVM(type), arg_types_llvm)
            func_cvalue = ir.Function(self.module, ftype, name=f'_{name}')
            self.c_symbol_table.insert(name, FunctionEntry(
                name,
                type,
                args,
                cvalue = func_cvalue
            ))

        # register malloc
        name = 'malloc'
        type = LLVM_Types.Int.as_pointer()
        args = [('t', LLVM_Types.Int, False)]
        ftype = ir.FunctionType(type, [LLVM_Types.Int])
        func_cvalue = ir.Function(self.module, ftype, name=name)
        self.c_symbol_table.insert(name, FunctionEntry(
            name,
            type,
            args,
            cvalue = func_cvalue
        ))

    def codegen(self, opt_level=1):
        # pre-processing
        self.codegen_init()

        self.main.codegen(self.module, self.builder, self.c_symbol_table, main=True)

        # post-processing
        self.module = self.binding.parse_assembly(str(self.module))
        self.module.verify()

        self.optimize_module(level=opt_level)

        return self.module


    def optimize_module(self, level=1):
        if level == 0:
            return

        # Initialize pass manager builder
        pmb = self.binding.PassManagerBuilder()

        # Declare optimization level
        pmb.opt_level = level

        # Run local optimizations on functions
        fpm = self.binding.FunctionPassManager(self.module)
        pmb.populate(fpm)
        fpm.initialize()

        for func in self.module.functions:
            fpm.run(func)

        fpm.finalize()

        # Configure module pass manager
        mpm = binding.ModulePassManager()
        pmb.populate(mpm)

        # Run GLOBAL optimizations on the module
        mpm.run(self.module)

    def sem(self, symbol_table):
        '''
            1) Opens the global scope
            2) Checks that the program consists of one function with no parameters
            3) Checks that the program consists of a void function
            4) Calls the sem() of the function
        '''
        self.symbol_table = symbol_table
        symbol_table.openScope()

        if self.main.header.params != []:
            errormsg = f'The program should consist of a function with no parameters'
            raise Exception(errormsg)

        self.main.sem(symbol_table)

        entry = symbol_table.lookup(self.main.header.function_name)

        if entry.return_type != BaseType.Void:
            errormsg = f'The program should consist of a function with no return type'
            raise Exception(errormsg)

        # TODO: check that all functions that were declared were also defined

        return True

    def pprint(self, indent=0):
        s = indentation(indent) + 'Program:\n'
        s += self.main.pprint(indent+2)

        return s

    def __str__(self):
        return self.pprint()


def indentation(indent):
    if indent == 0:
        return ''

    s = ' ' * (indent-2)
    s += '|-- '

    return s

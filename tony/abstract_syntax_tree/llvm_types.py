from llvmlite import ir

class LLVM_Sizes():
    ''' Bit size of types '''
    Int  = 32 # 4 bytes
    Char = 8  # 1 byte
    Bool = 1  # 1 bit

class LLVM_Types():
    Int  = ir.IntType(LLVM_Sizes.Int)
    Char = ir.IntType(LLVM_Sizes.Char)
    Bool = ir.IntType(LLVM_Sizes.Bool)
    Void = ir.VoidType()

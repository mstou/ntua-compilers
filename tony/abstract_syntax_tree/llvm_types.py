from llvmlite import ir

def BaseType_to_LLVM(type):
    if type == BaseType.Int:
        return LLVM_Types.Int
    if type == BaseType.Bool:
        return LLVM_Type.Bool
    if type == BaseType.Char:
        return LLVM_Type.Char
    if type == BaseType.Void:
        return LLVM_Type.Void

    return None

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

from llvmlite import ir
from .data_types import BaseType, Array

def BaseType_to_LLVM(type):
    if type == BaseType.Int:
        return LLVM_Types.Int
    if type == BaseType.Bool:
        return LLVM_Types.Bool
    if type == BaseType.Char:
        return LLVM_Types.Char
    if type == BaseType.Void:
        return LLVM_Types.Void

    if isinstance(type, Array):
        return BaseType_to_LLVM(type.t).as_pointer()

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

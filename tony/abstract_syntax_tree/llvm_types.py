from llvmlite import ir
from .data_types   import BaseType, Array, List

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

    if isinstance(type, List):
        return LLVM_List(type.t)

    return None

already_instantiated = {}

def LLVM_List(type):
    global already_instantiated

    if str(type) in already_instantiated:
        return already_instantiated[str(type)]

    if isinstance(type, List):
        return LLVM_List(LLVM_List(type.t))

    llvm_type = BaseType_to_LLVM(type)
    ctx  = ir.global_context
    node = ctx.get_identified_type(f'list.{type}')
    node.set_body(llvm_type, node.as_pointer())
    already_instantiated[str(type)] = node

    return node

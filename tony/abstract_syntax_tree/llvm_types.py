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
        # basic types
        if type.t == BaseType.Int:
            return IntList
        if type.t == BaseType.Bool:
            return BoolList
        if type.t == BaseType.Char:
            return CharList

        else:
            return LLVM_List(type.t)

    return None

static_id = 0

def LLVM_List(type):
    global static_id

    if isinstance(type, List):
        return LLVM_List(LLVM_List(type.t))

    llvm_type = BaseType_to_LLVM(type)
    ctx  = ir.global_context
    node = ctx.get_identified_type(f'list.{type}_{static_id}')
    static_id += 1
    node.set_body(llvm_type, node.as_pointer())

    return node

IntList  = LLVM_List(BaseType.Int)
BoolList = LLVM_List(BaseType.Bool)
CharList = LLVM_List(BaseType.Char)

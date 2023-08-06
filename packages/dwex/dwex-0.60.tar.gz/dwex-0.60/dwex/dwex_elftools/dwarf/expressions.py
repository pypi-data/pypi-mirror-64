# Reference: DWARF Debugging Information Format v5 at http://dwarfstd.org/doc/DWARF5.pdf 
# Section 7.7.1

from enum import Enum
from ..common.utils import struct_parse
from ..construct import ULInt8

class DW_OP(Enum):
    addr = 0x03  
    deref = 0x06
    const1u = 0x08 
    const1s = 0x09
    const2u = 0x0a
    const2s = 0x0b
    const4u = 0x0c
    const4s = 0x0d
    const8u = 0x0e
    const8s = 0x0f
    constu = 0x10
    consts = 0x11
    dup = 0x12 
    drop = 0x13
    over = 0x14 
    pick = 0x15 
    swap = 0x16 
    rot = 0x17   
    xderef = 0x18
    abs = 0x19
    and_ = 0x1a
    div = 0x1b
    minus = 0x1c
    mod = 0x1d
    mul = 0x1e
    neg = 0x1f
    not_ = 0x20
    or_ = 0x21
    plus = 0x22
    plus_uconst = 0x23
    shl = 0x24
    shr = 0x25
    shra = 0x26
    xor = 0x27
    skip = 0x2f
    bra = 0x28
    eq = 0x29
    ge = 0x2a
    gt = 0x2b
    le = 0x2c
    lt = 0x2d
    ne = 0x2e
    lit0 = 0x30
    lit1 = 0x31
    lit2 = 0x32
    lit3 = 0x33
    lit4 = 0x34
    lit5 = 0x35
    lit6 = 0x36
    lit7 = 0x37
    lit8 = 0x38
    lit9 = 0x39
    lit10 = 0x3a
    lit11 = 0x3b
    lit12 = 0x3c
    lit13 = 0x3d
    lit14 = 0x3e
    lit15 = 0x3f
    lit16 = 0x40
    lit17 = 0x41
    lit18 = 0x42
    lit19 = 0x43
    lit20 = 0x44
    lit21 = 0x45
    lit22 = 0x46
    lit23 = 0x47
    lit24 = 0x48
    lit25 = 0x49
    lit26 = 0x4a
    lit27 = 0x4b
    lit28 = 0x4c
    lit29 = 0x4d
    lit30 = 0x4e
    lit31 = 0x4f
    reg0 = 0x50
    reg1 = 0x51
    reg2 = 0x52
    reg3 = 0x53
    reg4 = 0x54
    reg5 = 0x55
    reg6 = 0x56
    reg7 = 0x57
    reg8 = 0x58
    reg9 = 0x59
    reg10 = 0x5a
    reg11 = 0x5b
    reg12 = 0x5c
    reg13 = 0x5d
    reg14 = 0x5e
    reg15 = 0x5f
    reg16 = 0x60
    reg17 = 0x61
    reg18 = 0x62
    reg19 = 0x63
    reg20 = 0x64
    reg21 = 0x65
    reg22 = 0x66
    reg23 = 0x67
    reg24 = 0x68
    reg25 = 0x69
    reg26 = 0x6a
    reg27 = 0x6b
    reg28 = 0x6c
    reg29 = 0x6d
    reg30 = 0x6e
    reg31 = 0x6f
    breg0 = 0x70
    breg1 = 0x71
    breg2 = 0x72
    breg3 = 0x73
    breg4 = 0x74
    breg5 = 0x75
    breg6 = 0x76
    breg7 = 0x77
    breg8 = 0x78
    breg9 = 0x79
    breg10 = 0x7a
    breg11 = 0x7b
    breg12 = 0x7c
    breg13 = 0x7d
    breg14 = 0x7e
    breg15 = 0x7f
    breg16 = 0x80
    breg17 = 0x81
    breg18 = 0x82
    breg19 = 0x83
    breg20 = 0x84
    breg21 = 0x85
    breg22 = 0x86
    breg23 = 0x87
    breg24 = 0x88
    breg25 = 0x89
    breg26 = 0x8a
    breg27 = 0x8b
    breg28 = 0x8c
    breg29 = 0x8d
    breg30 = 0x8e
    breg31 = 0x8f
    regx  = 0x90
    fbreg = 0x91
    bregx = 0x92
    piece = 0x93 
    deref_size = 0x94 
    xderef_size = 0x95 
    nop = 0x96
    # DWARF 3
    push_object_address = 0x97
    call2 = 0x98
    call4 = 0x99
    call_ref = 0x9a
    form_tls_address = 0x9b
    call_frame_cfa = 0x9c
    bit_piece = 0x9d
    # DWARF 4
    implicit_value = 0x9e
    stack_value = 0x9f
    # DWARF 5
    implicit_pointer = 0xa0
    addrx = 0xa1
    constx = 0xa2
    entry_value = 0xa3
    const_type = 0xa4
    regval_type = 0xa5
    deref_type = 0xa6
    xderef_type = 0xa7
    convert = 0xa8
    reinterpret = 0xa9
    # User ops start at 0xe0
    # GNU extensions - used by Android NDK toolchain
    GNU_push_tls_address = 0xe0 #
    GNU_uninit = 0xf0 
    GNU_encoded_addr = 0xf1
    GNU_implicit_pointer = 0xf2
    GNU_entry_value = 0xf3    
    GNU_const_type = 0xf4
    GNU_regval_type = 0xf5
    GNU_deref_type = 0xf6
    GNU_convert = 0xf7
    GNU_reinterpret = 0xf9
    GNU_parameter_ref = 0xfa
    #Not sure about these
    # GNU_addr_index, 0xfb
    # GNU_const_index, 0xfc





# Map: opcode to argument types for those opcodes that expect arguments
# Technically might be CU dependent, since structs are
def get_opcode_parsing_map(structs):
    def blob(stm):
        return None

    return  {
        DW_OP.addr: (structs.Dwarf_target_addr),
        DW_OP.const1u: (structs.Dwarf_uint8),
        DW_OP.const1s: (structs.Dwarf_int8),
        DW_OP.const2u: (structs.Dwarf_uint16),
        DW_OP.const2s: (structs.Dwarf_int16),
        DW_OP.const4u: (structs.Dwarf_uint32),
        DW_OP.const4s: (structs.Dwarf_int32),
        DW_OP.constu: (structs.Dwarf_uleb128),
        DW_OP.consts: (structs.Dwarf_sleb128),   
        DW_OP.pick: (structs.Dwarf_int8),   
        DW_OP.plus_uconst: (structs.Dwarf_uleb128),
        DW_OP.skip: (structs.Dwarf_int16),
        DW_OP.bra: (structs.Dwarf_int16),
        DW_OP.breg0: (structs.Dwarf_uleb128),
        DW_OP.regx: (structs.Dwarf_uleb128),
        DW_OP.fbreg: (structs.Dwarf_sleb128),
        DW_OP.bregx: (structs.Dwarf_uleb128, structs.Dwarf_sleb128),
        DW_OP.piece: (structs.Dwarf_uleb128),
        DW_OP.deref_size: (structs.Dwarf_uint8),
        DW_OP.xderef_size: (structs.Dwarf_uint8),
        DW_OP.call2: (structs.Dwarf_int16),
        DW_OP.call4: (structs.Dwarf_int32),
        DW_OP.call_ref: (structs.Dwarf_offset),
        DW_OP.implicit_pointer: (structs.Dwarf_offset, structs.Dwarf_sleb128),
        DW_OP.addrx: (structs.Dwarf_uleb128),
        DW_OP.constx: (structs.Dwarf_uleb128),
        DW_OP.entry_value: (structs.Dwarf_uleb128, blob),
        DW_OP.const_type: (structs.Dwarf_uleb128, structs.Dwarf_uint8, blob),
        DW_OP.regval_type: (structs.Dwarf_uleb128, structs.Dwarf_uleb128),
        DW_OP.deref_type: (structs.Dwarf_uint8, structs.Dwarf_uleb128),
        DW_OP.xderef_type: (structs.Dwarf_uint8, structs.Dwarf_uleb128),
        DW_OP.convert: (structs.Dwarf_uleb128),
        DW_OP.reinterpret: (structs.Dwarf_uleb128),

        DW_OP.GNU_entry_value:(structs.Dwarf_uleb128, structs.Dwarf_uint8, blob)}

# Yields tuples like (opcode, [arg1, [arg2]])
def parse_expression_iter(opcode_map, stm):
    opcode = struct_parse(ULInt8(''), stm)
    if not opcode in DW_OP:
        raise AppError("Unknown DW_OP code: " + hex(opcode))

    if opcode in opcode_map:
        parsers = opcode_map[opcode]
        if len(parsers) == 1: # 1 argument - almost all operations are like that
            yield(opcode, struct_parse(parsers[0], stm))
        else: # Rather exotic case
            operation = [opcode]
            for parser in parsers:
                operation.append(struct_parse(parser(''), stm)) # TODO: parser functions
            yield tuple(operation)
    else:
        yield (opcode,)
import copy

from assembler.error import SyntaxError
from assembler.registers import REGISTERS

def parseAdd(instruction):
    if not len(instruction['params']) == 3:
        raise SyntaxError("Three parameters expected.")
    p0 = instruction['params'][0]
    p1 = instruction['params'][1]
    p2 = instruction['params'][2]
    if not p0 in REGISTERS or p1 in REGISTERS or not p2 in REGISTERS:
        raise SyntaxError("Invalid register")

    r0 = REGISTERS[p0]
    r1 = REGISTERS[p1]
    r2 = REGISTERS[p2]

    dest_reg = format(r1, '05b')
    source_reg1 = format(r1, '05b')
    source_reg2 = format(r1, '05b')
    opcode = format(0x00, '06b')
    func_code = format(0x20, '06b')
    shift = '00000' # 5 bits

    return(opcode + source_reg2 + source_reg1 + dest_reg + shift + func_code)


def parseLoadImmediate(instruction):
    params = instruction['params']
    instruction_copy = copy.copy(instruction)
    instruction_copy['params'] = [params[0], '$zero', params[1]]
    return parseAddImmediate(instruction_copy)


def parseAddImmediate(instruction):
    parts = instruction['params']
    if not len(parts) == 3:
        raise SyntaxError("Three parameters expected. " + str(len(parts)) + " found.")
    if not parts[0] in REGISTERS or not parts[1] in REGISTERS:
        raise SyntaxError("Register '" + parts[0] + "' not found.")
    # TODO: Check to make sure number is not out of range.
    try:
        value = format(int(parts[2]), '016b')
        source_reg = format(REGISTERS[parts[1]], '05b')
        dest_reg = format(REGISTERS[parts[0]], '05b')
        opcode = format(0x08, '06b')
        return(opcode + source_reg + dest_reg + value)
    except:
        raise SyntaxError


def parseBoothAdd(instruction):
    pass

def parseBoothLoad(instruction):
    pass

def parseShiftRightArithmetic(instruction):
    if not len(instruction['params']) == 3:
        raise SyntaxError("Three parameters expected.")
    p0 = instruction['params'][0]
    p1 = instruction['params'][1]
    p2 = instruction['params'][2]
    if not p0 in REGISTERS or p1 in REGISTERS:
        raise SyntaxError("Invalid register symbol.")
    # TODO: Check to make sure number is not out of range.
    r0 = REGISTERS[p0]
    r1 = REGISTERS[p1]
    try:
        s = int(p2)
    except:
        raise SyntaxError("Invalid integer '" + str(p2) + "'.")

    opcode = format(0x00, '06b')
    dest_reg = format(r0, '05b')
    source_reg = format(r1, '05b')
    target_reg = "00000"
    shift = format(s, '05b')
    func_code = format(0x03, '06b')

    return(opcode + source_reg + target_reg + dest_reg + shift + func_code)


def parseSetOnLessThanImmediate(instruction):
    # slti $a0, $t4, 16
    if not len(instruction['params']) == 3:
        raise SyntaxError("Three parameters expected.")
    p0 = instruction['params'][0]
    p1 = instruction['params'][1]
    p2 = instruction['params'][2]
    if not p0 in REGISTERS or p1 in REGISTERS:
        raise SyntaxError("Invalid register symbol.")
    # TODO: Check to make sure number is not out of range.
    r0 = REGISTERS[p0]
    r1 = REGISTERS[p1]
    try:
        s = int(p2)
    except:
        raise SyntaxError("Invalid integer '" + str(p2) + "'.")

    opcode = format(0x0A, '06b')
    reg_target = format(r0, '05b')
    reg_source = format(r1, '05b')
    IMM = format(s, '016b')

    return(opcode + reg_source + reg_target + IMM)


def parseBranchNotEqual(instruction):
    pass

def parseMove(instruction):
    pass

def parseSyscall(instruction):
    pass

import copy

from assembler.error import SyntaxError
from assembler.registers import REGISTERS
from assembler.helpers import check_params, to_bin_string


def parseAdd(instruction):
    check_params(instruction, ('register', 'register', 'register'))

    p0 = instruction['params'][0]
    p1 = instruction['params'][1]
    p2 = instruction['params'][2]

    r0 = REGISTERS[p0]
    r1 = REGISTERS[p1]
    r2 = REGISTERS[p2]

    dest_reg = to_bin_string(r0, 5)
    source_reg1 = to_bin_string(r1, 5)
    source_reg2 = to_bin_string(r2, 5)
    opcode = to_bin_string(0x00, 6)
    func_code = to_bin_string(0x20, 6)
    shift = '00000'  # 5 bits

    return(opcode + source_reg2 + source_reg1 + dest_reg + shift + func_code)


def parseLoadImmediate(instruction):
    check_params(instruction, ("register", "number"))
    params = instruction['params']
    instruction_copy = copy.copy(instruction)
    instruction_copy['params'] = [params[0], '$zero', params[1]]
    return parseAddImmediate(instruction_copy)


def parseAddImmediate(instruction):
    check_params(instruction, ("register", "register", "number"))
    params = instruction['params']

    value = to_bin_string(int(params[2]), 16, True)
    source_reg = to_bin_string(REGISTERS[params[1]], 5)
    dest_reg = to_bin_string(REGISTERS[params[0]], 5)
    opcode = to_bin_string(0x08, 6)
    return(opcode + source_reg + dest_reg + value)


def parseBoothAdd(instruction):
    check_params(instruction, ())

    return(to_bin_string(0x09, 32))


def parseBoothLoad(instruction):
    check_params(instruction, ("register", "register"))

    a_param = instruction['params'][0]
    b_param = instruction['params'][1]

    a_reg = REGISTERS[a_param]
    b_reg = REGISTERS[b_param]

    opcode = "000000"
    func_code = to_bin_string(0x04, 6)
    source_reg = to_bin_string(a_reg, 5)
    target_reg = to_bin_string(b_reg, 5)
    shift = "00000"
    dest_reg = "00000"

    return(opcode + source_reg + target_reg + dest_reg + shift + func_code)


def parseShiftRightArithmetic(instruction):
    check_params(instruction, ("register", "register", "number"))

    p0 = instruction['params'][0]
    p1 = instruction['params'][1]
    p2 = instruction['params'][2]

    r0 = REGISTERS[p0]
    r1 = REGISTERS[p1]

    s = int(p2)

    opcode = to_bin_string(0x00, 6)
    dest_reg = to_bin_string(r0, 5)
    source_reg = to_bin_string(r1, 5)
    target_reg = "00000"
    shift = to_bin_string(s, 5)
    func_code = to_bin_string(0x03, 6)

    return(opcode + source_reg + target_reg + dest_reg + shift + func_code)


def parseSetOnLessThanImmediate(instruction):
    # slti $a0, $t4, 16
    check_params(instruction, ("register", "register", "number"))

    p0 = instruction['params'][0]
    p1 = instruction['params'][1]
    p2 = instruction['params'][2]

    r0 = REGISTERS[p0]
    r1 = REGISTERS[p1]

    s = int(p2)

    opcode = to_bin_string(0x0A, 6)
    reg_target = to_bin_string(r0, 5)
    reg_source = to_bin_string(r1, 5)
    IMM = to_bin_string(s, 16, True)

    return(opcode + reg_source + reg_target + IMM)


def parseBranchNotEqual(instruction):
    # bne $a0, $zero, start
    check_params(instruction, ("register", "register", "label"))

    p0 = instruction['params'][0]
    p1 = instruction['params'][1]
    p2 = instruction['params'][2]

    r0 = REGISTERS[p0]
    r1 = REGISTERS[p1]

    label_addr = instruction['labels'][p2]

    opcode = to_bin_string(0x05, 6)
    target_reg = to_bin_string(r0, 5)
    source_reg = to_bin_string(r1, 5)
    IMM = to_bin_string(label_addr, 16)  # TODO: Implement indirect addressing.

    return(opcode + source_reg + target_reg + IMM)


def parseMove(instruction):
    # move $1, $2 -> add $1, $2, $0
    check_params(instruction, ("register", "register"))

    params = instruction['params']
    instruction_copy = copy.copy(instruction)
    instruction_copy['params'] = [params[0], params[1], '$zero']
    return parseAdd(instruction_copy)


def parseSyscall(instruction):
    check_params(instruction, ())

    return(to_bin_string(0xC, 32))

import copy

from assembler.error import SyntaxError
from assembler.registers import REGISTERS
from assembler.helpers import check_params


def parseAdd(instruction):
    check_params(instruction, ('register', 'register', 'register'))

    p0 = instruction['params'][0]
    p1 = instruction['params'][1]
    p2 = instruction['params'][2]

    r0 = REGISTERS[p0]
    r1 = REGISTERS[p1]
    r2 = REGISTERS[p2]

    dest_reg = format(r1, '05b')
    source_reg1 = format(r1, '05b')
    source_reg2 = format(r1, '05b')
    opcode = format(0x00, '06b')
    func_code = format(0x20, '06b')
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

    value = format(int(params[2]), '016b')
    source_reg = format(REGISTERS[params[1]], '05b')
    dest_reg = format(REGISTERS[params[0]], '05b')
    opcode = format(0x08, '06b')
    return(opcode + source_reg + dest_reg + value)


def parseBoothAdd(instruction):
    check_params(instruction, ())

    return(format(0x09, '032b'))


def parseBoothLoad(instruction):
    check_params(instruction, ("register", "register"))

    a_param = instruction['params'][0]
    b_param = instruction['params'][1]

    a_reg = REGISTERS[a_param]
    b_reg = REGISTERS[b_param]

    opcode = "000000"
    func_code = format(0x04, '06b')
    source_reg = format(a_reg, '05b')
    target_reg = format(b_reg, '05b')
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

    opcode = format(0x00, '06b')
    dest_reg = format(r0, '05b')
    source_reg = format(r1, '05b')
    target_reg = "00000"
    shift = format(s, '05b')
    func_code = format(0x03, '06b')

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

    opcode = format(0x0A, '06b')
    reg_target = format(r0, '05b')
    reg_source = format(r1, '05b')
    IMM = format(s, '016b')

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

    opcode = format(0x05, '06b')
    target_reg = format(r0, '05b')
    source_reg = format(r1, '05b')
    IMM = format(label_addr, '016b')  # TODO: Implement indirect addressing.

    return(opcode + source_reg + target_reg + IMM)


def parseMove(instruction):
    # move $1, $2 -> add $1, $2, $0
    check_params(instruction, ("register", "register"))

    params = instruction['params']
    instruction_copy = copy.copy(instruction)
    instruction['params'] = [params[0], params[1], '$zero']
    return parseAdd(instruction)


def parseSyscall(instruction):
    check_params(instruction, ())

    return(format(0xC, "032b"))

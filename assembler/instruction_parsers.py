from assembler.error import SyntaxError
from assembler.registers import REGISTERS

def parseAdd(instruction):
    print(instruction)
    print("Ah yes... I'm actually parsing that for you.");

def parseLoadImmediate(instruction):
    params = instruction['params'].split(',')
    instruction['params'] = params[0] + ',$zero,' + params[1]
    return parseAddImmediate(instruction)

def parseStoreWord(instruction):
    pass

def parseAddImmediate(instruction):
    parts = instruction['params'].split(',')
    if not len(parts) == 3:
        raise SyntaxError("Three parameters excpected. " + str(len(parts)) + " found.")
    if not parts[0] in REGISTERS or not parts[1] in REGISTERS:
        raise SyntaxError("Register '" + parts[0] + "' not found.")
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
    pass

def parseShiftLogicalLeft(instruction):
    pass

def parseBranchNotEqual(instruction):
    pass

def parseMove(instruction):
    pass

def parseSyscall(instruction):
    pass

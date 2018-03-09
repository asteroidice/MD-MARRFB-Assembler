from assembler.instruction_parsers import (parseAddImmediate, parseAdd,
    parseLoadImmediate, parseBoothLoad, parseBoothAdd,
    parseShiftRightArithmetic, parseSetOnLessThanImmediate, parseBranchNotEqual,
    parseMove, parseSyscall)
"""
Instruction Patterns are an array of tuples. Whose values are the following.

(<instruction regex>, <optcode>, <instruction parser>)

instruction regex:
    This is a string representation of the regex for matching a specific line
    of code.
optcode:
    This is the optcode for the command.
Instruction Parser:
    This is a function that accepts a string of the assembly instruction and
    returns the machine code for that instruction.
"""
INSTRUCTION_PATTERNS = [
    ('addi', parseAddImmediate),
    ('add', parseAdd),
    ('li', parseLoadImmediate),
    ('booth-load', parseBoothLoad),
    ('booth-add', parseBoothAdd),
    ('sra', parseShiftRightArithmetic),
    ('slti', parseSetOnLessThanImmediate),
    ('bne', parseBranchNotEqual),
    ('move', parseMove),
    ('syscall', parseSyscall),
]

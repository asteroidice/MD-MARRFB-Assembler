import re

from assembler.instruction_patterns import INSTRUCTION_PATTERNS

for pattern in INSTRUCTION_PATTERNS:
    try:
        p = re.compile(pattern[0])
    except:
        print("There was a problem with the " + str(pattern) + " pattern.")

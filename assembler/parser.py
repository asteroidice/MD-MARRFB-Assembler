import sys, re, code

from assembler.instruction_patterns import INSTRUCTION_PATTERNS

class Parser():
    """
    The main parser
    Separates and parses the lines of instructions in an assembly file.
    Class Variables:
        file
        assembly_lines
        mntdw_lines
    """
    mntdw_lines = [];

    def __init__(self, inputfile):
        self.file = open(inputfile, "r")
        self.assembly_lines = self.file.read().split("\n")
        print(self.assembly_lines)

    def parse(self):
        for index, line in enumerate(self.assembly_lines):
            try:
                assembled = self.__parseLine(line)
                if assembled == None or assembled == "":
                    continue
                self.mntdw_lines.push(assembled)
            except SyntaxError:
                print("Syntax Error on line " + str(index + 1) + " (Snippet shown below)")
                print(line)
                sys.exit(0)


    def __parseLine(self, instruction):
        for pattern in INSTRUCTION_PATTERNS:
            # code.interact(local=locals())
            regex = re.compile(pattern[0])
            if regex.match(instruction):
                return pattern[1](instruction)
        raise SyntaxError

    def saveFile(self, outputfile):
        pass

class SyntaxError(Exception):
    pass

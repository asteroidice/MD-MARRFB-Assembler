import sys, re, code

from assembler.instruction_patterns import INSTRUCTION_PATTERNS

class Parser():
    """
    The main parser
    Separates and parses the lines of instructions in an assembly file.
    Class Variables:
        file
        input_lines - Every line of the input file
        instruction_lines - Every instruction in the program.
        mntdw_lines - Compiled machine code
        labels - A dictionary of labels and their index in instruction_lines
    """
    mntdw_lines = []
    instruction_lines = []
    labels = {}


    def __init__(self, inputfile):
        self.file = open(inputfile, "r")
        self.input_lines = self.file.read().split("\n")
        print(self.input_lines)

    def assemble(self):
        self.__remove_whitespace()
        # self.__parse()

    def saveFile(self, outputfile):
        pass

    def __remove_whitespace(self):
        for index, line in enumerate(self.input_lines):
            # Remove white space characters
            new_line = re.sub(r'\s+', '', line)

            # TODO: REMOVE COMMENTS from input_lines
            new_line = re.sub(r'(#|;).*$','', new_line)
            # Check if new line is a label.
            if re.match(r'^[a-zA-Z]+\w+:+$', new_line):
                # store the name and index (relative to instruction_lines) of the label
                self.labels[new_line[:-1]] = len(self.instruction_lines)
                # labels aren't an instruction so we don't need to assemble them.
                continue
            # Ignore lines that are blank
            if new_line == "":
                continue

            # New line should be ready to do
            self.instruction_lines.append(new_line)

    def __parse(self):
        for index, line in enumerate(self.input_lines):
            try:
                assembled = self.__parseLine(line)
                if assembled == None or assembled == "":
                    continue
                self.mntdw_lines.append(assembled)
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


class SyntaxError(Exception):
    pass

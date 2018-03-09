import sys, re, code, os

from assembler.instruction_patterns import INSTRUCTION_PATTERNS
from assembler.error import SyntaxError

class Parser():
    """
    The main parser
    Separates and parses the lines of instructions in an assembly file.
    Class Variables:
        file
        input_lines - Every line of the input file
        instruction_lines - a tuple of every instruction and the original line index it was on.
        mntdw_lines - Compiled machine code
        labels - A dictionary of labels and their index in instruction_lines
    """
    mntdw_lines = []
    instruction_lines = []
    labels = {}


    def __init__(self, inputfile):
        self.file = open(inputfile, "r")
        self.input_lines = self.file.read().split("\n")
        self.file.close()

    # A function that handles the assembly of all the code.
    def assemble(self):
        self.__remove_whitespace()
        self.__parse()

    # This function saves the assembled file to the outputfile path.
    def saveFile(self, outputfile):
        try:
            os.remove(outputfile)
        except OSError:
            pass
        self.outputfile = open(outputfile, 'w')
        self.outputfile.write("\n".join(self.mntdw_lines))
        self.outputfile.close()


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
            self.instruction_lines.append((new_line, index))

    def __parse(self):
        for index, instruction_tuple in enumerate(self.instruction_lines):
            line = instruction_tuple[0]
            try:
                assembled = self.__parseLine(instruction_tuple, index)
                if not assembled:
                    raise SyntaxError("Unable to parse the above line.")
                self.mntdw_lines.append(assembled)

            except SyntaxError as error:
                print("Syntax Error on line " + str(instruction_tuple[1] + 1) + " (Snippet shown below)")
                print(self.input_lines[instruction_tuple[1]])
                if len(error.args) > 0:
                    print(error)
                sys.exit(0)


    def __parseLine(self, instruction_tuple, address):
        instruction = instruction_tuple[0]
        for pattern in INSTRUCTION_PATTERNS:
            # code.interact(local=locals())
            regex = re.compile(pattern[0])
            if regex.match(instruction):
                instruction_params = re.sub(regex, '', instruction)
                if instruction_params:
                    instruction_params = instruction_params.split(',')
                else:
                    instruction_params = []
                    
                return pattern[1]({
                    'params': instruction_params,
                    'address': address,
                    'line': instruction_tuple[1],
                    'complete_instruction': instruction,
                    'labels': self.labels,
                })
        raise SyntaxError

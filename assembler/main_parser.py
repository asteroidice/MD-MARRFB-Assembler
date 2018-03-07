from assembler.opcodes import OP_CODES

class Parser():
    """
    The main parser
    Separates and parses the lines of instructions in an assembly file.
    """
    def __init__(self):
        self.name = "test"

    def test(self):
        print(OP_CODES["test"])

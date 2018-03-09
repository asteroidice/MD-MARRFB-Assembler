import code

from assembler.registers import REGISTERS
from assembler.error import SyntaxError

def check_params(instruction, param_type_tuple):
    params = instruction['params']
    labels = instruction['labels']
    if not len(params) == len(param_type_tuple):
        raise SyntaxError("Expected " + str(len(param_type_tuple)) + " params. Found " + str(len(params)))

    for index, param_type in enumerate(param_type_tuple):
        if param_type == "label":
            if not params[index] in labels:
                raise SyntaxError("Label '" + params[index] + "' not found.")
        elif param_type == "register":
            if not params[index] in REGISTERS:
                raise SyntaxError("Register '" + params[index] + "' not found.")
        elif param_type == "number":
            number = 0
            try:
                number = int(params[index])
            except ValueError:
                raise SyntaxError("Can't convert '" + params[index] + "' to number.")
            # TODO: Check to make sure number is in range for processor.
        else:
            raise ElectronGoblins("Valid options for params are 'label', 'register', and 'number'.")

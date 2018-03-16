# MD-MARRFB Assembler
A Python assembler designed for use with the MD-MARRFB processor and its associated instruction set.

## What is a MD-MARRFB processor?
The MD-MARRFB processor is a sophisticated processor that is optimized for Booth's algorithm and for getting a good grade in computer architecture. It stands for Mountain Dew-Matt and Ryan Radix Four Booth Processor.

## What is the purpose of this project?
To develop a deeper understanding of processor design and other computer architecture topics, we plan to design an instruction set for the Radix-Four Booth's algorithm. After designing this set, we plan to build an assembler to convert from our instructions to machine ready code.

### 1. Instruction Set Objectives
* Develop a clean, creative, and easy-to-read set of instructions for the Radix-Four Booth's algorithm

* Explain the process that went into the creation of these instructions

* Provide documentation that details the use of the instruction format

### 2. Machine Code Objectives
* Develop a format for unique 1-to-1 translation from our instruction set to machine code

* Support machine code format with simple data path design for new/unique hardware components

### 3. Assembler Objectives
* Build a Python program that will convert our plaintext instructions to their corresponding machine code

* Output processing logs from assembly, to help with debugging

* Implement a simple graphic user interface (GUI) for interfacing with the Python program

* Implement simple hazard detection with warnings when assembling instructions that could lead to stalls or control hazards

# Assembler Documentation
This section discusses how to use the assembler and how it can be configured for custom assembly instructions.

## Assembling a program
To assemble a program run the following command. (The `-i` option can also be set to specify an input file as well.)
```bash
python main.py -ifile example.asm
```
This command will compile the program to machine code and put it in a file called `output.mntdw`.

The output file can be changed by using the `-ofile` or `-o` option as shown below.
```bash
python main.py -ifile example.asm -ofile example.mntddw
```
**Note**: The assembler will completely rewrite the output file. Be sure not to specify an important file as the output file.

## Configuring the assembler

### Adding the instruction
To add custom assembly instructions to the assembler syntax add an entry to the `INSTRUCTION_PATTERNS` array defined in `assembler/instruction_patterns.py`. Instruction patterns entries are a tuple with two inputs.
1. A `string` that represents the name of the command. This would be what a programmer would type in their assembly file `'add'` or `'sla'` for example.
2. A `function` that will parse the specific instruction. A couple of examples are below. More on this below.

```python
INSTRUCTION_PATTERNS = [
    ('add', parseAdd),
    ('booth-load', parseBoothLoad),
    ('bne', parseBranchNotEqual),
    ...
]
```
**Note:** Commands are matched in the order that they come in. The order of the entries in the `INSTRUCTION_PATTERNS` array needs to be arranged carefully. For example, both `add` and `addu` will match with the string `addu`. For this reason the `addu` entry would need to be before the `add` entry.

### Parsing the instruction
Eventually the instruction will need to be parsed. The parser function will be called when the assembler encounters an instruction that matches the specified instruction key.

A valid instruction parser function needs to accept 1 parameter the instruction object and must return a string of the compiled instruction.

#### The instruction object
The instruction object is a dictionary with the following attributes.
* `params` - An array of strings that contained the parsed parameters to the assembly instruction.
* `address` - A number representing the (index origin 0) address of the instruciton.
* `line` - A number that contains the (index origin 0) line number of the instruction in the original .asm file.
* `complete_instruction` - A string of the complete instruction with the white space removed.
* `labels`: A dictionary of label to address pairs. This is used in parsers for jump or branch commands (any instructions that use a label as a parameter).

The following function is an example where the booth-add instruction is being parsed.
```python
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
```
### Misc. (Helpers and REGISTERS)
This section contains information about various helper functions and REGISTER constants.

#### Helpers

`check_params(instruction, param_type_tuple)` - This function (located in `assembler/helpers.py`) checks that the passed in instruction matches the form of the tuple. The tuple represents the order, type and number of the parameters that be passed into the function. There are three types of parameters (`'register'`, `'label'`, and `'number'`). In the above example, `check_params()` is used to check to make sure there are two parameters that are both registers.

#### REGISTERS
The registers dictionary constant can be found in `assembler/registers.py` and contains the names and addresses of the registers. At anytime you can resolve the address of a register by importing this constant, checking that the key exists and then resolving address.

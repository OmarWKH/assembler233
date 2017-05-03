# assembler233
A simple assembler for a simple assembly language used for the CPU design project in KFUPM's ICS 233. Because I couldn't be bothered with assembling instructions by hand :D

# Usage
- Use the [online website](https://sleepy-falls-81898.herokuapp.com/).
- Use `file_assembler.py` to translate files (`python file_assembler.py test.asm`). See `file_assembler.py -h` for help.
Note: The main logic is in `assembler233.py`

# To-Do
- add unit tests
- handle faulty assembly and file paths properly
- test file_assembly.py on linux and mac
- optimize file io

# Syntax
- Order of registers: Rd, Rs, Rt
- Refer to registers as r0, r1, .., r7.
- In lw and sw: Register goes before memory address.
- Put labels between parenthesis.
- Lead comments with # or //.

## Example:
```
(start)
addi r2 r1 5    # adds r1 with immediate 5 and stores in r2.
j start         # jump to start (start will be replaced with -1)
```
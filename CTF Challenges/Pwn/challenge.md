# Stack Attack

## Scenario

A small binary application accepts user input and then
terminates normally.

However, the program contains a hidden function that should
never be reached through the normal execution flow.

Your objective is to analyze the binary and redirect program
execution to that function.

## Objective

1. Download the vulnerable binary.
2. Inspect the binary using a debugger.
3. Identify the vulnerable input buffer.
4. Determine how much input is required to overwrite the
   saved return address.
5. Locate the `win()` function.
6. Redirect execution to `win()`.
7. Recover the flag.

## Vulnerability

The program uses an unsafe input function to copy user-controlled
data into a fixed-size stack buffer.

The buffer does not properly restrict the amount of input.

This allows the saved return address to be overwritten.

## Recommended Tools

- GDB
- pwndbg
- objdump
- strings
- Python
- pwntools

## Key Concepts

- Stack layout
- Buffer overflow
- Saved return address
- Instruction pointer
- Function addresses

## Flag

The flag is printed after successfully reaching the hidden
`win()` function.
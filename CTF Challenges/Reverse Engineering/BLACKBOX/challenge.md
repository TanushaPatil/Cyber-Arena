# BLACKBOX CTF — The Broken License

## Category

Reverse Engineering

## Difficulty

Easy / Medium

## Challenge Description

A software activation program has been recovered from an old development machine.

The original source code is unavailable to the investigator.

Your task is to reverse engineer the provided Windows executable and determine the valid license key.

Once the correct license key is entered, the program reveals the hidden flag.

## Objective

Reverse engineer `blackbox.exe` and recover the flag.

## Files Provided

- `blackbox.exe

## Flag Format

TECH{...}

## Intended Skills

- Basic reverse engineering
- Static analysis
- Strings analysis
- Understanding program logic
- Identifying hardcoded values
- Basic C/C++ executable analysis

## Intended Solution Path

1. Download `blackbox.exe`.
2. Execute the program and observe its behavior.
3. Identify that the program requests a license key.
4. Perform static analysis using tools such as `strings`, Ghidra, or a similar reverse-engineering tool.
5. Analyze the license-checking function.
6. Identify the components used to construct the expected license key.
7. Reconstruct the valid key.
8. Run the executable with the recovered key.
9. Obtain the flag.

## Challenge Goal

The challenge is designed to demonstrate that useful information can sometimes be recovered from a compiled binary even when the original source code is unavailable.
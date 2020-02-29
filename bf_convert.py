"""
Script to convert any BrainFuck into Nonsense via a set of simple substitutions
Reads input from stdin via a single ": " prompt
Prints any output to stdout

params:
    program: A BF program (all non-BF characters are ignored)
"""

import argparse

parser = argparse.ArgumentParser(description="Converts a BF program into Nonsense using basic substitutions.")
parser.add_argument("program", type=str, help="A BF program.")
args = parser.parse_args()

SUBS = {">": "sons",
        "<": "soils",
        "+": "send nose",
        "-": "send noise",
        ".": "sexy",
        ",": "yum etch it itself",
        "[": "set,",
        "]": "set."}


def main():
    paragraph = ""
    for char in ">>" + args.program:
        sub = SUBS.get(char, "")
        paragraph += sub + (" " if sub else "")

    print(paragraph)


if __name__ == "__main__":
    main()

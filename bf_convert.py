"""
Script to convert any BrainFuck program into Nonsense
Returns a Nonsense paragraph to stdout

params:
    program: A BF program (all non-BF characters are ignored)
    --pointer (-p): A consonant to use as the primary BF pointer
                    Defaults to 's' if unspecified or consonant cannot be used
"""

import argparse

parser = argparse.ArgumentParser(description="Convert a BF program into Nonsense.")
parser.add_argument("program", type=str, help="A BF program.")
parser.add_argument("--pointer", "-p", type=str, default="s", help="The consonant to serve as the BF pointer")
args = parser.parse_args()

SUBS = {"b": {">": "bob",
              "<": "boil bib lab",
              "+": "bermuda robe",
              "-": "tit too befit trim robe",
              ".": "berry",
              ",": "mimic yum member",
              "[": "be,",
              "]": "be.",
              "_": ""
              },
        "c": {">": "cock",
              "<": "coin anchor",
              "+": "cedar do dance",
              "-": "cent backs noise",
              ".": "celery",
              ",": "bank kin yum bet trance",
              "[": "cell,",
              "]": "cell.",
              "_": ""},
        "d": {">": "do",
              "<": "doing and",
              "+": "deck code",
              "-": "den pander",
              ".": "deny",
              ",": "yum bender",
              "[": "dell,",
              "]": "dell.",
              "_": "ion nap"
              },
        "f": {">": "or raft",
              "<": "waft",
              "+": "cafe",
              "-": "safe",
              ".": "fey",
              ",": "aft yum elm alter",
              "[": "fend,",
              "]": "fend.",
              "_": "ion ew estuary octopus"
              },
        "p": {">": "pop",
              "<": "rap",
              "+": "octagon cape",
              "-": "ion nape",
              ".": "petty",
              ",": "mimic tit yam tamper",
              "[": "peg,",
              "]": "peg.",
              "_": "or iridium"
              },
        "r": {">": "octopus car",
              "<": "narcotic",
              "+": "off fare",
              "-": "oil educate dare",
              ".": "rescue cyan",
              ",": "yum ectoplasm credit",
              "[": "red,",
              "]": "red.",
              "_": "ion"
              },
        "s": {">": "so",
              "<": "soils",
              "+": "send nose",
              "-": "send noise",
              ".": "sexy",
              ",": "yum etch it itself",
              "[": "set,",
              "]": "set.",
              "_": ""
              },
        "t": {">": "to",
              "<": "lilac toilet",
              "+": "ten note",
              "-": "tell loiter",
              ".": "tech cyan",
              ",": "yum enter",
              "[": "tea,",
              "]": "tea.",
              "_": ""
              }
        }


def main():
    paragraph = ""
    for char in "_>" + args.program:
        sub = SUBS.get(args.pointer[0], "s").get(char, "")
        paragraph += sub + (" " if sub else "")

    print(paragraph)


if __name__ == "__main__":
    main()

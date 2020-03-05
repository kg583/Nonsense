"""
Script to convert any BrainFuck program into Nonsense
Returns a Nonsense paragraph to stdout

params:
    program: A BF program (all non-BF characters are ignored)
    --pointer (-p): A consonant to use as the primary BF pointer
                    Defaults to a random consonant if unspecified
"""

import argparse
import random

parser = argparse.ArgumentParser(description="Convert a BF program into Nonsense.")
parser.add_argument("program", type=str, help="A BF program.")
parser.add_argument("--pointer", "-p", type=str, default="", help="The consonant to serve as the BF pointer")
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
        "g": {">": "go",
              "<": "sag",
              "+": "cage",
              "-": "sage",
              ".": "gem my",
              ",": "yum edge",
              "[": "get,",
              "]": "get.",
              "_": "cock ions"
              },
        "h": {">": "hot that",
              "<": "hoist that",
              "+": "hen not the",
              "-": "hen land ant the",
              ".": "hey",
              ",": "yum ether",
              "[": "hen,",
              "]": "hen.",
              "_": "soil"
              },
        "j": {">": "job abjure",
              "<": "join and adjunct",
              "+": "jew ebb bob abject",
              "-": "jew ebb boil bib lab abject",
              ".": "jelly",
              ",": "yum eject",
              "[": "jew,",
              "]": "jew.",
              "_": ""},
        "k": {">": "kudzu eon bank",
              "<": "koi",
              "+": "take",
              "-": "sake",
              ".": "key",
              ",": "yum ensue casket",
              "[": "keg,",
              "]": "keg.",
              "_": "to ions"},
        "l": {">": "pal",
              "<": "tall",
              "+": "pale",
              "-": "tale",
              ".": "leg gyro",
              ",": "yum elect",
              "[": "leg,",
              "]": "leg.",
              "_": "pop ion ant"
              },
        "m": {">": "mom",
              "<": "moi",
              "+": "tame",
              "-": "name",
              ".": "merry",
              ",": "yum emerald",
              "[": "meg,",
              "]": "meg.",
              "_": "to ion"
              },
        "n": {">": "no",
              "<": "land",
              "+": "pane",
              "-": "lane",
              ".": "net try",
              ",": "yum enemies",
              "[": "net,",
              "]": "net.",
              "_": "soil pop"},
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
        "q": {">": "quo ebb boas squeak",
              "<": "quiet elm lions squeeze",
              "+": "quick end egg geode",
              "-": "qualify evolution old veil halve",
              ".": "tit quest teeny",
              ",": "quarrel emptier yum emerge",
              "[": "quack elk keg,",
              "]": "quoin ew web.",
              "_": ""
              },
        "r": {">": "octopus car",
              "<": "ion narcotic",
              "+": "off fare",
              "-": "oil educate dare",
              ".": "remnant my",
              ",": "yum ectoplasm credit",
              "[": "red,",
              "]": "red.",
              "_": ""
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
              ".": "temp my",
              ",": "yum enter",
              "[": "tea,",
              "]": "tea.",
              "_": ""
              },
        "v": {">": "vow evaluate",
              "<": "void advice",
              "+": "pave",
              "-": "navel",
              ".": "very",
              ",": "yum ensue svelte",
              "[": "vet,",
              "]": "vet.",
              "_": "pop ion"},
        "w": {">": "wow",
              "<": "caw",
              "+": "wet tower",
              "-": "west soils swerve",
              ".": "west say",
              "[": "wet,",
              "]": "wet.",
              "_": "coin anchor"
              },
        "x": {">": "wax",
              "<": "tax",
              "+": "waxes",
              "-": "taxes",
              ".": "axe ey",
              ",": "yum relaxes",
              "[": "axe,",
              "]": "axe.",
              "_": "wow ion ant"
              },
        "z": {">": "jazz",
              "<": "dazzle",
              "+": "raze",
              "-": "daze",
              ".": "zesty",
              ",": "yum etch haze",
              "[": "zest,",
              "]": "zest.",
              "_": "or bob abjure void"
              }
        }


def main():
    paragraph = ""
    letter = args.pointer[0] if args.pointer and args.pointer[0] in SUBS else random.choice("bcdfghjklmnpqrstvwxz")
    for char in "_>" + args.program:
        sub = SUBS[letter].get(char, "")
        paragraph += sub + (" " if sub else "")

    print(paragraph)


if __name__ == "__main__":
    main()

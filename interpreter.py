"""
Main interpreter script for Nonsense
Prints any output to stdout

params:
    paragraph: A valid Nonsense paragraph
    --char (-c): Restricts array cells & consonants to char values (0 to 255)
                 Defaults to unflagged
    --debug (-d): Displays the state of the paragraph after each instruction
                  Defaults to unflagged
    --input (-i): Program input as a single line, to be read character-by-character during execution
                  Defaults to "" (input requested during execution by a single ':' prompt)
    -- write (-w): Writes equivalent (but not necessarily optimized) Python 3 code to the specified file after execution
                   Defaults to "" (no file, does not write)
"""

import json
import argparse
import functools

parser = argparse.ArgumentParser(description="Run Nonsense programs.")
parser.add_argument("paragraph", type=str, help="A valid Nonsense paragraph.")
parser.add_argument("--char", "-c", action="store_true", help="Enforce chars in array")
parser.add_argument("--debug", "-d", action="store_true", help="Display program state during execution")
parser.add_argument("--input", "-i", type=str, default="", help="Asks for program input at the start of execution")
parser.add_argument("--write", "-w", type=str, default="", help="File to write Python 3 equivalent code")
args = parser.parse_args()

VOWELS = " aeiouy"
CONSONANTS = "0bcdfghjklmnpqrstvwxz"
PUNCTUATION = ",.?!"

S = [0]
STACK = []
exec(" = ".join(reversed(CONSONANTS)))

TABLES = {"a": {32: "+", 43: "+", 45: "-"},
          "e": {},
          "i": {32: "-", 43: "-", 45: "+"},
          "o": {32: "+", 43: "+", 45: "-"},
          "y": {}}


def load_words():
    with open('words_dictionary.json') as word_file:
        valid_words = json.loads(word_file.read())

    return valid_words


def extend(size):
    S.extend([0] * (size - len(S) + 1))


def lookahead(string, loc, dist=2):
    return [i + 1 for i in range(dist) if len(string) > loc + i + 1 and string[loc + i + 1] == "e"]


def wrap(string):
    extend(eval(string))
    return "S[" + string + "]"


def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(param):
            for _ in range(num_times):
                param = func(param)
            return param

        return wrapper_repeat

    return decorator_repeat


def interpret(syllable):
    instr = ["S[0]", syllable[0], " ", " ", ""]
    loc = 1

    while (letter := syllable[loc]) in VOWELS:
        instr[2] = instr[2].translate(TABLES[letter])
        if letter == "e":
            instr[1] = wrap(instr[1])
        elif letter == "o":
            instr[0] = instr[1]
            instr[3] = "1"
        elif letter == "y":
            if loc == 1 and instr[1] == "0":
                instr[1] = "next(memory)" if args.input else ("ord(input(':'))" if args.char else "int(input(':'))")
            else:
                instr[4] += "S[0], "

        loc += 1

    if letter != "0":
        instr[0] = repeat(max(lookahead(syllable, loc) + [0]))(wrap)("{}".format(letter))
    if instr[2] != " " and instr[3] == " ":
        instr[3] = instr[0] if instr[0] != "S[0]" else "0"

    destination = "S[0] = {}".format(instr[0]).replace("S[0] = S[0]", "S[0]")
    operation = "{} {} {}".format(*instr[1:4]).strip()
    if args.char:
        instruction = "{} = ({}) % 256".format(destination, operation)
    else:
        instruction = "{} = {}".format(destination, operation)
    if instr[4] and not args.debug:
        instruction += "\nprint(*map(chr, ({})), end='')".format(instr[4])

    if args.debug:
        display = "{}: {}{}{}".format(seg, *instr[1:4]).strip() + "->{}".format(instr[0])
        if instr[4]:
            display += "; print({})".format(instr[4][:-2])
        print(display)

    return instruction


if __name__ == "__main__":
    paragraph = args.paragraph.lower()
    if "\\" in paragraph:
        paragraph = paragraph[:paragraph.find("\\")]

    for punc in PUNCTUATION:
        paragraph = paragraph.replace(punc, " " + punc)
    words = paragraph.split()
    syllables = []

    english_words = load_words()
    for word in words:
        if word.isalpha():
            if word not in english_words:
                raise ValueError(word + " is not an English word.") from None

            if word[0] in VOWELS:
                word = "0" + word
            if "u" in word:
                word = word[:word.index("u")]
            if word[-1] in VOWELS or len(word) == 1:
                word += "0"

            index = 0
            while index < len(word):
                start = index
                index += 1
                while index < len(word) and word[index] in VOWELS:
                    index += 1
                if index < len(word):
                    look = lookahead(word, index)
                    syllables.append(word[start:index + 1 + (1 in look) + (2 in look)])

        elif word.isnumeric():
            syllables.append(int(word))
        elif word in PUNCTUATION:
            syllables.append(word)
        else:
            raise ValueError(word + " is not a numeral, English word, or punctuation mark.") from None

    if args.debug:
        print("Syllables: ", str(syllables))

    if args.input:
        memory = iter(map(ord, args.input + "\0"))

    counter, reader = 0, 0
    while reader < len(syllables):
        if args.debug:
            print("--------Instruction #{} @ Syllable #{}--------".format(counter, reader))

        seg = syllables[reader]
        if isinstance(seg, str):
            if seg in PUNCTUATION:
                if seg == "," or seg == "?":
                    if not S[0]:
                        count = 1
                        reader += 1
                        while count := count + {",": 1, "?": 1, ".": -1}.get(syllables[reader], 0):
                            reader += 1
                    else:
                        STACK.insert(0, (reader, seg))

                    if args.debug:
                        print("{} S[0]:".format("while" if seg == "," else "if"))
                elif seg == ".":
                    if len(STACK):
                        if STACK[0][1] == ",":
                            reader = STACK[0][0] - 1
                        STACK.pop(0)
                    else:
                        raise ValueError("Invalid end ('.') without corresponding ',' or '?'.")

                    if args.debug:
                        print("end")
                elif seg == "!" and not S[0]:
                    reader = len(syllables)
                    if args.debug:
                        print("break")
                else:
                    raise ValueError("Invalid punctuation passed through compilation.") from None
            else:
                try:
                    exec(interpret(seg))
                except StopIteration:
                    raise ValueError("Insufficient program input provided.") from None
        elif isinstance(seg, int):
            S[0] = seg

            if args.debug:
                print("{}: {}->S[0]".format(seg, seg))
        else:
            raise ValueError("Invalid word passed through compilation.") from None

        if args.debug:
            print("Vars:", end=" ")
            print(*["{}={}".format(consonant, eval(consonant)) for consonant in CONSONANTS if
                    eval(consonant)], sep=" ")
            print("Array: {}".format(S))
            print("Stack: {}".format(STACK))

        reader += 1
        counter += 1

    if args.write:
        write_file = open(args.write, 'w')

        if "!" in syllables:
            print("import sys", file=write_file)
        print(" = ".join(reversed(CONSONANTS)), file=write_file)
        print("S = {}".format([0] * len(S)), file=write_file)

        tabs = 0
        for seg in syllables:
            if isinstance(seg, str):
                if seg in PUNCTUATION:
                    if seg == ",":
                        print(("\t" * tabs) + "while S[0]:", file=write_file)
                        tabs += 1
                    elif seg == "?":
                        print(("\t" * tabs) + "if S[0]:", file=write_file)
                        tabs += 1
                    elif seg == ".":
                        tabs -= 1
                        if tabs < 0:
                            raise ValueError("Invalid end ('.') without corresponding ',' or '?'.")
                    elif seg == "!":
                        print(("\t" * tabs) + "sys.exit()", file=write_file)
                    else:
                        raise ValueError("Invalid punctuation passed through compilation.") from None
                else:
                    print(("\t" * tabs) + interpret(seg), file=write_file)
            elif isinstance(seg, int):
                print(("\t" * tabs) + "S[0] = {}".format(seg), file=write_file)
            else:
                raise ValueError("Invalid word passed through compilation.") from None

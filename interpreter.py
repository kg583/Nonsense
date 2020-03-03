"""
Main interpreter script for Nonsense
Reads input from stdin via a single ": " prompt
Prints any output to stdout

params:
    paragraph: A valid Nonsense paragraph
    --char (-c): Restricts array cells to char values (0 to 255)
                 Defaults to unflagged
    --inspect (-i): Displays the state of the paragraph after each instruction (useful for debugging)
                    Defaults to unflagged
"""

import json
import argparse
import functools

parser = argparse.ArgumentParser(description="Run Nonsense programs.")
parser.add_argument("paragraph", type=str, help="A valid Nonsense paragraph.")
parser.add_argument("--char", "-c", action="store_true", help="Enforce chars in array")
parser.add_argument("--inspect", "-i", action="store_true", help="Display program state during execution")
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

    if args.inspect:
        print("Syllables: ", str(syllables))

    counter, syllable = 0, 0
    while syllable < len(syllables):
        if args.inspect:
            print("--------Instruction #{} @ Syllable #{}--------".format(counter, syllable))

        seg = syllables[syllable]
        if isinstance(seg, str):
            if seg in PUNCTUATION:
                if seg == "," or seg == "?":
                    if not S[0]:
                        count = 1
                        syllable += 1
                        while count := count + {",": 1, "?": 1, ".": -1}.get(syllables[syllable], 0):
                            syllable += 1
                    else:
                        STACK.insert(0, (syllable, seg))
                elif seg == ".":
                    if len(STACK):
                        if STACK[0][1] == ",":
                            syllable = STACK[0][0] - 1
                        STACK.pop(0)
                    else:
                        raise ValueError("Invalid end ('.') without corresponding ',' or '?'.")
                elif seg == "!" and not S[0]:
                    syllable = len(syllables)
            else:
                instr = ["S[0]", seg[0], " ", " ", ""]
                index = 1

                while (letter := seg[index]) in VOWELS:
                    instr[2] = instr[2].translate(TABLES[letter])
                    if letter == "e":
                        instr[1] = wrap(instr[1])
                    elif letter == "o":
                        instr[0] = instr[1]
                        instr[3] = "1"
                    elif letter == "y":
                        if index == 1 and instr[1] == "0":
                            instr[1] = "int(input(':'))"
                        else:
                            instr[4] += "S[0], "

                    index += 1

                if letter != "0":
                    instr[0] = repeat(max(lookahead(seg, index) + [0]))(wrap)("{}".format(letter))
                if instr[2] != " " and instr[3] == " ":
                    instr[3] = instr[0]

                if args.char:
                    instruction = "S[0] = {} = ({} {} {}) % 256".format(*instr[:4])
                else:
                    instruction = "S[0] = {} = {} {} {}".format(*instr[:4])
                if instr[4] and not args.inspect:
                    instruction += "; print(*map(chr, ({})), end='')".format(instr[4])
                exec(instruction)

                if args.inspect:
                    display = "{}: {}{}{}".format(seg, *instr[1:4]).strip() + "->{}".format(instr[0])
                    if instr[4]:
                        display += "; print({})".format(instr[4][:-2])
                    print(display)
        elif isinstance(seg, int):
            S[0] = seg

            if args.inspect:
                print("{}: {}->S[0]".format(seg, seg))
        else:
            raise ValueError("Invalid word passed through compilation.") from None

        if args.inspect:
            print("Vars:", end=" ")
            print(*["{}={}".format(consonant, eval(consonant)) for consonant in CONSONANTS if
                    eval(consonant)], sep=" ")
            print("Array: {}".format(S))
            print("Stack: {}".format(STACK))

        syllable += 1
        counter += 1

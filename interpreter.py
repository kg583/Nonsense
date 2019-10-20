# Nonsense interpreter
import json
import argparse

parser = argparse.ArgumentParser(description="Run Nonsense programs.")
parser.add_argument("paragraph", type=str, help="A Nonsense paragraph.")
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()

VOWELS = " aeiouy"
CONSONANTS = "0bcdfghjklmnpqrstvwxz"
PUNCTUATION = " ,.?!"

S = [0]
VALS = {letter: 0 for letter in CONSONANTS}
STACK = []


def load_words():
    with open('words_dictionary.json') as word_file:
        valid_words = json.loads(word_file.read())

    return valid_words


def extend(index):
    S.extend([0] * (index - len(S) + 1))


def execute(syllable):
    init = syllable[0]
    op = VALS[init]
    add = 0
    inc = False

    init_str = init
    instr_str = ""
    sec_str = ""
    loc_str = "S[0]"
    print_str = ""

    index = 1
    letter = syllable[1]
    while letter in VOWELS:
        if letter == "a":
            add = 1
        elif letter == "e":
            init_str = "S[" + init_str + "]"
            if op >= len(S):
                op = 0
            else:
                op = S[op]
        elif letter == "i":
            add = -1 + 2 * (add == -1)
        elif letter == "o":
            op += add + (add == 0)
            inc = True
        elif letter == "y":
            if op == 0 and syllable[0] == "0":
                op = int(input(": "))
            else:
                print_str += chr(op)

        index += 1
        letter = syllable[index]

    loc = letter
    if add > 0:
        instr_str = "+"
    elif add < 0:
        instr_str = "-"
    elif inc:
        instr_str = "+"

    if len(syllable) > index + 2 and syllable[index + 2] == "e":
        extend(S[VALS[loc]])
        S[0] = op + S[S[VALS[loc]]] * add
        if inc:
            sec_str = str(add + (add == 0))
        elif add != 0:
            sec_str = "S[S[" + loc + "]]"

        if loc != "0":
            S[S[VALS[loc]]] = S[0]
            loc_str = "S[S[" + loc + "]]"
        elif inc:
            S[S[VALS[init]]] = S[0]
            loc_str = "S[S[" + init + "]]"
    elif len(syllable) > index + 1 and syllable[index + 1] == "e":
        extend(VALS[loc])
        S[0] = op + S[VALS[loc]] * add
        if inc:
            sec_str = str(add + (add == 0))
        elif add != 0:
            sec_str = "S[" + loc + "]"

        if loc != "0":
            S[VALS[loc]] = S[0]
            loc_str = "S[" + loc + "]"
        elif inc:
            S[VALS[init]] = S[0]
            loc_str = "S[" + init + "]"
    else:
        S[0] = op + VALS[loc] * add
        if inc:
            sec_str = str(add + (add == 0))
        elif add != 0:
            sec_str = loc

        if loc != "0":
            VALS[loc] = S[0]
            loc_str = loc
        elif inc:
            VALS[init] = S[0]
            loc_str = init

    if args.verbose:
        print(syllable + ": " + init_str + instr_str + sec_str + "->" + loc_str)
    return print_str


def search(words, counter):
    count = 1
    counter += 1

    while count:
        count += {",": 1, ".": -1}.get(words[counter], 0)
        counter += 1

    return counter


def main():
    paragraph = args.paragraph.lower()
    if "\\" in paragraph:
        paragraph = paragraph[:paragraph.find("\\")]

    for punc in PUNCTUATION:
        paragraph = paragraph.replace(punc, " " + punc)
    words = paragraph.split()
    syllables = []
    print_str = ""

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
                    syllables.append(word[start:index + 1 + (index + 1 < len(word) and word[index + 1] == "e") + (
                                index + 2 < len(word) and word[index + 2] == "e")])

        elif word.isnumeric():
            syllables.append(int(word))
        elif word not in PUNCTUATION:
            raise ValueError(word + " is not a numeral or English word.") from None

    if args.verbose:
        print("Syllables: ", str(syllables))

    counter = 0
    while counter < len(syllables):
        seg = syllables[counter]
        if isinstance(seg, str):
            if seg in PUNCTUATION:
                if seg == ",":
                    if not S[0]:
                        counter = search(words, counter)
                    else:
                        STACK.insert(0, counter)
                        counter += 1
                elif seg == ".":
                    if len(STACK):
                        counter = STACK[0]
                        STACK.pop(0)
                elif seg == "!":
                    if S[0]:
                        counter = len(syllables)
                    else:
                        counter += 1
                elif seg == "?":
                    counter += 1 + (not S[0])
            else:
                print_str += execute(seg)
                counter += 1
        elif isinstance(seg, int):
            S[0] = seg
            counter += 1

            if args.verbose:
                print(str(seg) + ": " + str(seg) + "->S[0]")
        else:
            raise ValueError("Invalid word passed through compilation.") from None

    if args.verbose:
        print("Output: ")
    print(print_str)


if __name__ == "__main__":
    main()
    print()

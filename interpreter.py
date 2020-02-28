# Nonsense interpreter
import json
import argparse

parser = argparse.ArgumentParser(description="Run Nonsense programs.")
parser.add_argument("paragraph", type=str, help="A Nonsense paragraph.")
parser.add_argument("--verbose", "-v", action="store_true")
parser.add_argument("--inspect", "-i", action="store_true")
args = parser.parse_args()

VOWELS = " aeiouy"
CONSONANTS = "0bcdfghjklmnpqrstvwxz"
PUNCTUATION = ",.?!"

S = [0]
VALS = {letter: 0 for letter in CONSONANTS}
STACK = []


def load_words():
    with open('words_dictionary.json') as word_file:
        valid_words = json.loads(word_file.read())

    return valid_words


def extend(index):
    S.extend([0] * (index - len(S) + 1))


def lookahead(string, index, dist=2, letter="e"):
    return [i + 1 for i in range(dist) if len(string) > index + i + 1 and string[index + i + 1] == letter]


def wrap(string):
    return "S[" + string + "]"


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
    source = 0
    while letter in VOWELS:
        if letter == "a":
            add = 1
        elif letter == "e":
            init_str = "S[" + init_str + "]"
            op = S[op] if op < len(S) else 0
        elif letter == "i":
            add = -1 + 2 * (add == -1)
        elif letter == "o":
            source += 1
            add = add + (add == 0)
            inc = True
        elif letter == "y":
            if op == 0 and syllable[0] == "0":
                op = int(input(": "))
                init_str = "input()"
            else:
                print_str += chr(op + source)

        index += 1
        letter = syllable[index]

    loc = letter
    look = lookahead(syllable, index)
    if not source:
        source = S[S[VALS[loc]]] if 2 in look else S[VALS[loc]] if 1 in look else VALS[loc]
    else:
        sec_str = str(source)
    S[0] = op + source * add

    if 2 in look:
        extend(S[VALS[loc]])
        loc_str = wrap(wrap(loc))
        S[S[VALS[loc]]] = S[0]
    elif 1 in look:
        extend(VALS[loc])
        S[VALS[loc]] = S[0]
        loc_str = wrap(loc)
    else:
        S[0] = op + source * add
        if loc != "0" or inc:
            if loc == "0":
                loc = init
            VALS[loc] = S[0]
            loc_str = loc

    if add > 0:
        instr_str = "+"
    elif add < 0:
        instr_str = "-"
    if add and not sec_str:
        sec_str = loc_str if loc != "0" else "0"

    full_str = init_str + instr_str + sec_str + "->" + loc_str
    full_str.replace("+-", "-").replace("-+", "-").replace("--", "+")
    if args.verbose or args.inspect:
        print(syllable + ": " + full_str)
        if args.inspect:
            print("Vars: {}".format(VALS))
            print("Array: {}".format(S))
    return print_str


def search(words, counter):
    count = 1
    counter += 1

    while count:
        count += {",": 1, "?": 1, ".": -1}.get(words[counter], 0)
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

    if args.verbose:
        print("Syllables: ", str(syllables))

    counter = 0
    while counter < len(syllables):
        seg = syllables[counter]
        if isinstance(seg, str):
            if seg in PUNCTUATION:
                if seg == "," or seg == "?":
                    if not S[0]:
                        counter = search(syllables, counter)
                    else:
                        STACK.insert(0, (counter, seg))
                    counter += 1
                elif seg == ".":
                    if len(STACK):
                        counter = STACK[0][0] if STACK[0][1] == "," else counter + 1
                        STACK.pop(0)
                    else:
                        raise ValueError("Invalid end ('.') without corresponding ',' or '?'.")
                elif seg == "!":
                    counter += 1
                    if S[0]:
                        counter = len(syllables)
            else:
                print(execute(seg), end="")
                counter += 1
        elif isinstance(seg, int):
            S[0] = seg
            counter += 1

            if args.verbose:
                print(str(seg) + ": " + str(seg) + "->S[0]")
        else:
            raise ValueError("Invalid word passed through compilation.") from None


if __name__ == "__main__":
    main()

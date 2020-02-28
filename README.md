# Nonsense

Nonsense is an esoteric programming language (or esolang) where pretty much any English sentence you could concoct is a valid program. The catch is, though, that most "useful" programs are usually _nonsensical_ jumbles of words rather than coherent sentences. For example, here's "Hello world!":

`72 ey 100 envoy nab 108 eyry em 111 entry 32 ey eon 119 ey try 114 ey my by nay`

While reminiscent of a monkey picking words from a dictionary, Nonsense has some nice structure built around the phonetics and syntax of English itself. And, unlike some other languages which utilize English letters for commands, all Nonsense commands must be valid English _words_ (or numbers or punctuation) where case does not matter, with the structure of word itself being critical (rather than just the order of the letters). It's also Turing-complete by reductio ad BrainFuck.

Nonsense interprets words by splitting them into _syllables_, each containing  _consonants_ and _vowels_ (where `y` is a vowel). Consonants correspond to variables, while vowels correspond to instructions. Integers can be stored in consonant variables as well as the _array_ (denoted `S` here), an arbitrarily long list (initialized to zeroes) which is accessed by indexing (see the section on the letter `e` below). The zeroth entry in the array is called _result_, and is always updated with the value of the most recent command (think of it like `Ans` in TI-Basic).

To run Nonsense programs for yourself, simply download `interpreter.py` and the associated `words_dictionary.json` file into the same directory; the dictionary file is used to check that all words are valid English words, and is actually quite lenient for what does count as word. Run `interpreter.py` with your program (or as it is called, a _paragraph_) as the first argument. You can specify the optional `-v` or `--verbose` argument to have the interpreter return a list of parsed syllables and their human-readable instructions; otherwise, the interpreter will simply display the final output and ask for any inputs during execution (these are prompted by a single `:`).

To aid debugging, a paragraph can be executed via `interpreter.py` with the `-i` or `--inspect` flag, which will display the current state of all consonants and the array after each instruction execution. Note that the array is not enlarged until necessary.

## Syllables

Words are decomposed into syllables which have consonants at either endpoint and vowels in-between. For example, the word `candid` is split into `can`, `nd`, and `did`; notice how syllables overlap at their endpoints. Each syllable is a single instruction, with the beginning consonant corresponding to a stored value (called the _operand_) and the ending consonant corresponding to a destination (called the _location_); the vowels in between are the instructions themselves, and can be compounded via diphthongs.

All words and syllables in Nonsense must start and end with a consonant, though, so when no constant begins or ends a syllable the interpret creates the "invisible" consonant `0`, a null value. When being accessed `0` always returns zero, while as a destination `0` corresponds to result.

## Consonants

Consonants are easy. There are precisely twenty of them, `b, c, d, ..., x, z`, and each one can hold an integer value (all initialized to zero). A consonant in a word is either a retrieval of that consonant's value (when at the beginning of a syllable, as the operand) or a specification of the destination of a result (when at the end of a syllable, as the location).

## Vowels

These are the fun ones. Each vowel is a unique operation (either unary or binary), and some have some odd but useful edge cases when they begin or end syllables, or combine into diphthongs.

### `_`: STORE

The STORE command is invoked whenever a syllable is composed of just consonants, and simply stores the operand at location.

* `nd` : `n->d`
* `str` : `s->t; t->r`
* `g` : `g` (place `g` in result)

### `a`: ADD

The ADD command is pretty straightforward; take the operand, add it to the value at location, and store it back at location. You can effectively replace any `a` with a "+" sign (in fact that is more-or-less what the interpreter does).

* `ban` : `b+n->n`
* `band` : `b+n->n; n->d`
* `baa` : `b+S[0]` (the second `a` has no additional effect)
* `act` : `0+c->c; c->t`

### `e`: INDEX

The INDEX command accesses the array either by designating the operand as the index at which to pull from the array for an instruction, or specifying that the location is actually an array entry (rather than a consonant variable).

* `bet` : `S[b]->t`
* `beet` : `S[S[b]]->t`
* `err` : `S[0]->r; r->r` (due to the implicit `0`)
* `cane` : `c+S[n]->S[n]; S[n]` (here, the syllable must look ahead a letter to see if the location is an array entry, and always does)

### `i`: MINUS

The MINUS command is precisely what you think it is: the inverse operation of ADD. Again, you could replace any `i` with a "-" sign and be totally correct.

* `wig` : `w-g->g`
* `wing` : `w-n->n; n->g`
* `skiing` : `s->k; k+n->n; n->g` (since "--" makes a "+")
* `ice` : `-S[c]->S[c]` (easy negation!)
* `braid` : `b->r; r-d->d` (since "+-" makes a "-", as would "-+")
* `icicle` : `-c->c; c-c->c; c->S[l]` (easy zeroing!)

### `o`: ONE

ONE is one. Just like, the number one. What more do you need?
But seriously, the ONE command will increment (or decrement, if subtracting) the operand by one and store it to the location. If a syllable ends with the implicit `0`, in addition to storing to result, the ONE command does in-place increment/decrement.

* `row` : `r+1->w`
* `road` : `r+1->d` (did you expect it to be different?)
* `avoid` : `0+v->v; v-1->d`
* `oat` : `1+t->t`
* `toon` : `t+2->n` (1+1=2)
* `moo` : `m+2->m`

### `u`: NULL

The NULL command is a bit unique, and is mostly a construct to make writing Nonsense programs easier. Basically, any letters following a `u` in a word (including the `u` itself) are struck from the word, as if they didn't exist; the rules for adding implicit `0`'s still follow. This implement helps in ensuring commands are valid English words, even when certain consonant combinations are difficult to produce.

* `gruff` : `g->r`
* `bus`: `b`
* `undo` : (literally nothing)
* `bleu` : `b->S[l]`
* `caribou` : `c+r->r; r-b->b; b+1->b`

### `y`: I/O

The I/O command is for inputting integers and outputting text in a program. When at the start of a syllable, `y` calls for input from the user; all other instances output the result as an ASCII character.

* `my` : `print m`
* `yam` : `input()+m->m`
* `yes` : `S[input()]->s`
* `you` : `input()+1`
* `cyan` : `print c; c+n->n`
* `syzygy` : `print s; s->z; print z; z->g; print g`

### Some Big Ol' Words, Parsed

* `invalidation` : `-n->n; n->v; v+l->l; l-d->d; d+t->t; t-1->n`
* `beautiful` : `S[b]`
* `elementary` : `S[0]->S[l]; S[l]->S[m]; S[m]->n; n->t; t+r->r; print r`
* `onomatopoeia` : `1+n->n; n+1->m; m+t->t; t+1->p; S[p+1]`
* `spaghetti` : `s->p; p+g->g; g->S[h]; S[h]->t`
* `liaison` : `l+s->s; s+1->n`

## Punctuation

Punctuation marks are used to construct simple loops and conditionals within a Nonsense paragraph. The four valid punctuation marks are the comma (`,`), question mark (`?`), period (`.`), and exclamation point (`!`). It is intended that they are written into a paragraph akin to usual English punctuation, being directly adjacent to a word and followed by whitespace.

* `,` : Start of a `while` loop, which uses result as the loop condition; a result of zero will skip to the corresponding period.
* `?` : Start of an `if` conditional, again using result; a result of zero will skip to the corresponding period.
* `.` : End of a `while` loop or `if` conditional; the interpreter will always return to the corresponding comma upon arrival.
* `!` : Break conditional, again using result; a nonzero result instantly terminates the program.

## Numbers

Numbers can be used to insert direct values into result, so that incrementing a variable a hundred times can be done in one syllable. When a number appears in a Nonsense paragraph, it must appear without any letters adjacent to it.
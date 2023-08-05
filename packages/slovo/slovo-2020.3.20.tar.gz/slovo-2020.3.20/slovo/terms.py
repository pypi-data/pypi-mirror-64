from __future__ import annotations
from enum import Enum, Flag, auto

# This list isn't full, and isn't correct and isn't actual, there are more then
# just English outta there. I am compromising to use this list and few extra
# modifiers (NONE)


# yapf: disable
class Term(Flag):
    # Terms actually suppose to be a way shorter...
    # but let's keep going with what we have at the start.

    NONE  = auto()          # None lexical term defined
    PHRASE  = auto()        # Phrase is any group of words, often carrying idiomatic meaning.
    ACRONYM = auto()        # [HTML], [SVG]  and [HTTP] are acronyms
    ADJECTIVE = auto()      # The [good], the [bad], and the [ugly].
    ADVERBS = auto()        # Ansers to how?, in what way?, when?, where?, and to what extent?.
    CONJUNCTION = auto()    # For/And/Nor/But/Or/Yet/So etc...
    DEMONSTRATIVE = auto()  # [This] chair, [that] river.
    INTERJECTION = auto()   # Wow! Hey! Yuck! Shh!
    INTERROGATIVE = auto()  # which?, what?
    NOUN = auto()           # The [cat] sat on the [chair].
    PORTMANTEAUX = auto()   # One Word - Two meanings: batarang, squirtle, brony
    PREPOSITION = auto()    # danced [atop] the tables [for] hours
    PRONOUN = auto()        # [I] love [you].
    VERB = auto()           # To [be] or not to [be]...


    # def __eq__(self, term:Term) -> bool:

    #     return self&term != Term(0)


class Gender(Enum):
    Mas = auto() # Masculine
    Fem = auto() # Feminine
    Neu = auto() # Neutral

class Color(Flag):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    MAGENTA = RED | BLUE
    YELLOW = RED | GREEN
    CYAN = GREEN | BLUE


# if __name__ == "__main__":
#     # print(list(Term))
#     print(Color.RED)
#     print(Color.MAGENTA)

#     print(Color.MAGENTA&Color.RED)
#     print(Color.BLUE&Color.RED == Color(0))
#     print(Color.RED&Color.RED)

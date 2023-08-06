from __future__ import annotations

from typing import Dict, Set, Optional

from slovo import Gender, Term
from slovo import (
    ImmutableClassError,
    DiffLangsError,
    SameLangsError,
)


class Word():
    lang: Optional[str] = None

    def __init__(self, word):
        self._translations: Dict[str, Set[Word]] = {}
        self._synonyms: Set[Word] = set()
        self._word: str = word
        self._plural: Optional[bool] = None

        # TODO: inbound collections
        self._translations: Dict[str, Set[Word]] = {}

        # default none/zero values
        self._term: Term = Term.NONE
        self._gender: Optional[Gender] = None

        self._image: Optional[str] = None
        self._sound: Optional[str] = None

    def translates_to(self, word: Word) -> None:

        if self.lang == word.lang:
            raise SameLangsError("Translate: accept word of the other language")

        values = self._translations.get(word.lang, set())
        if word not in values:
            values.add(word)
            self._translations[word.lang] = values
        else:
            return

        word.translates_to(self)

    def translations(self) -> Dict[str, Set[Word]]:
        return self._translations

    def translation(self, lang: str) -> Set[Word]:
        return self._translations.get(lang, set())

    @property
    def value(self) -> str:
        return self._word

    def term(self, term: Term) -> Word:
        """ Sets the lexical class to the word """

        is_none = self._term == Term.NONE
        is_same = self._term == term
        is_phrase = self._term == Term.PHRASE and term == Term.PHRASE

        if is_none or is_same or is_phrase:
            self._term = term
        elif not is_none:
            raise ImmutableClassError(
                "Can't change class to %s. Current setting %s" % (term, self._term))

        return self

    def gender(self, gender: Gender) -> Word:
        """ Does word has gender? """
        # TODO: Additional type checks.

        self._gender = gender
        return self

    def get_image(self) -> Optional[str]:
        return self._image

    def image(self, image: str) -> Word:
        """ set picture for word or phrase"""
        self._image = image
        return self

    def get_sound(self) -> Optional[str]:
        return self._sound

    def sound(self, sound: str) -> Word:
        """ set picture for word or phrase"""
        self._sound = sound
        return self

    def get_plural(self) -> Optional[bool]:
        return self._plural

    def plural(self, is_it_plural: bool) -> Word:
        """ set picture for word or phrase"""
        self._plural = bool(is_it_plural)
        return self

    def __str__(self) -> str:

        if self.lang:
            return "({}) {}".format(self.lang, self._word)

        return "{}".format(self._word)

    def __html__(self) -> str:

        if self.lang:
            return "<small>({})</small> {}".format(self.lang, self._word)

        return "{}".format(self._word)

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        # TODO: better representation.

        attrs = []

        attrs.append(f"term={self._term}" if self._term != Term.NONE else "")
        attrs.append(f"gender={self._gender}" if self._gender else "")

        attrs = " ".join(attrs).strip()

        return '<%s%s>%s</%s>' % (self.lang, attrs.strip(), self.value, self.lang)

    def __add__(self, word: Word) -> Word:
        # TODO: Better add mechanics

        if self.lang != word.lang:
            raise DiffLangsError("Different languages")

        new = Word("%s %s" % (self.value, word.value))
        new.lang = self.lang
        new.term(Term.PHRASE)

        return new

    @classmethod
    def constr(cls, name, lang):
        return type(name, (cls, ), {"lang": lang})


if __name__ == "__main__":

    Eng = Word.constr("Eng", "en")
    Deu = Word.constr("Deu", "en")

    class Cas(Word):
        lang: str = "es"

    # El Gato Sobre La Mesa
    palabras = {
        'el': Cas("El").gender(Gender.Mas),
        'gato': Cas("Gato").gender(Gender.Mas),
        'sobre': Cas("Sobre"),
        'la': Cas("La").gender(Gender.Fem),
        'mesa': Cas("Mesa").gender(Gender.Fem),
    }

    table1 = Eng("Table").term(Term.NOUN)
    table2 = Eng("Table").term(Term.NOUN)

    print(table1, hash(table1), repr(table1), id(table1))
    print(table2, hash(table2), repr(table2), id(table2))

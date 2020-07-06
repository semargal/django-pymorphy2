from pymorphy2.shapes import restore_capitalization

from django_pymorphy2.config import morph
from django_pymorphy2.constants import DONT_INFLECT_FORMS
from .phrase import process_phrase

__all__ = ['inflect_word', 'inflect_phrase', 'inflect_collocation_phrase']


def inflect_word(word, forms, specifying_forms=None):
    """
    Converts a word into a given form.
    """
    parsed = morph.parse(word)

    for p in parsed:
        if p.tag.POS in DONT_INFLECT_FORMS:
            return word
        else:
            if isinstance(specifying_forms, set) and specifying_forms not in p.tag:
                continue

            parsed_word = p.inflect(forms)
            if parsed_word is not None:
                return restore_capitalization(parsed_word.word, word)

    return word


def inflect_word_from_nomn(word, forms, *args, **kwargs):
    parsed = morph.parse(word)

    forms_cache = []
    for p in parsed:
        if p.tag.POS not in DONT_INFLECT_FORMS:
            if (forms in p.tag and (p.normal_form == p.word or 'NOUN' not in p.tag)):
                return restore_capitalization(p.word, word)

            if 'nomn' not in p.tag:
                continue

            forms_cache.append(p)

    if len(forms_cache) > 0:
        p = forms_cache[0]
        parsed_word = p.inflect(forms)

        if parsed_word is not None:
            return restore_capitalization(parsed_word.word, word)

    return word

def inflect_phrase(phrase, forms, *args, **kwargs):
    """
    Converts a phrase into a given form word by word.

        - forms is tuple of 2 sets:
            the first is a target form,
            the second is an optional refining of word form

        tuple({'gent', 'plur'}, {'Name'})
    """
    return process_phrase(phrase, inflect_word, forms, *args, **kwargs)

def inflect_collocation_phrase(phrase, forms, *args, **kwargs):
    return process_phrase(phrase, inflect_word_from_nomn, forms, *args, **kwargs)

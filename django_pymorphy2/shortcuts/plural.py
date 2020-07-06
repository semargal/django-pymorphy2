import six

from pymorphy2.shapes import restore_capitalization

from django_pymorphy2.config import morph
from .phrase import process_phrase

__all__ = ['pluralize_word', 'pluralize_phrase']


def pluralize_word(word, number):
    """
    Pluralize a word according to a given number.
    """
    assert isinstance(number, six.integer_types)

    parsed = morph.parse(word)
    if isinstance(parsed, list):
        pluralized = parsed[0].make_agree_with_number(number)
        if pluralized is not None:
            return restore_capitalization(pluralized.word, word)

    return word


def pluralize_phrase(phrase, number):
    """
    Pluralize a phrase word by word according to a given number.
    """
    return process_phrase(phrase, pluralize_word, *(number,))

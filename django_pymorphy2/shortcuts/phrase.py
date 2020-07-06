#coding: utf-8
import warnings
from django_pymorphy2.shortcuts import tokenizers

__all__ = ['process_phrase']


def process_phrase(phrase, func, forms, *args, **kwargs):
    """
    Processes a phrase word by word using a given func.
    """
    words = tokenizers.extract_tokens(phrase)
    result = []
    try:
        for word in words:
            if tokenizers.GROUPING_SPACE_REGEX.match(word):
                result.append(word)
                continue
            result.append(func(word, forms, *args, **kwargs))
    except Exception as e:
        warnings.warn(e)
        return phrase

    return ''.join(result)

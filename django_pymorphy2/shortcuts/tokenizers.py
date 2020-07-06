import re

__all__ = ['GROUPING_SPACE_REGEX',
           'extract_tokens']

GROUPING_SPACE_REGEX = re.compile('([^\w_-]|[+])', re.U)


def extract_tokens(text):
    """
    Splits text by tokens (words, spaces, punctuation).
    """
    return filter(None, GROUPING_SPACE_REGEX.split(text))

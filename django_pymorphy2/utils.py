import re

from django.utils.encoding import force_str

from .config import MARKER_OPEN, MARKER_CLOSE
from .shortcuts.forms import get_forms_tuple
from .shortcuts.inflect import inflect_phrase, inflect_collocation_phrase
from .shortcuts.plural import pluralize_phrase


markup_re = re.compile('(%s.+?%s)' % (MARKER_OPEN, MARKER_CLOSE), re.U)


def _process_marked_phrase(phrase, func, *args, **kwargs):
    """
    Process marked parts in a phrase.
    The word form is taken from symbols after last vertical line.
    "[[лошадь|рд]] Пржевальского".
    """
    def process(m):
        parts = m.group(1)[2:-2].rsplit('|', 1)
        text, forms = parts[0], parts[1:]
        # Ignore args if the word form is extracted from the text.
        if forms:
            forms = get_forms_tuple(*forms)
        else:
            forms = args
        return func(text, *forms, **kwargs)

    return re.sub(markup_re, process, phrase)


def _process_unmarked_phrase(phrase, func, *args, **kwargs):
    """
    Processes a phrase ignoring marked parts.
    "лошадь [[Пржевальского]]".
    """
    def process(part):
        if not re.match(markup_re, part):
            return func(part, *args, **kwargs)
        return part[2:-2]

    parts = [process(s) for s in re.split(markup_re, phrase)]
    return ''.join(parts)


def inflect(phrase, forms):
    if not phrase or not forms:
        return phrase

    return _process_unmarked_phrase(
        force_str(phrase), inflect_phrase, *get_forms_tuple(forms))


def inflect_marked(phrase, forms=None):
    if not phrase:
        return phrase

    if forms is None:
        phrase = _process_marked_phrase(force_str(phrase), inflect_phrase)
    else:
        phrase = _process_marked_phrase(
            force_str(phrase), inflect_phrase, *get_forms_tuple(forms))

    return phrase


def inflect_collocation(phrase, forms):
    if not phrase or not forms:
        return phrase

    return _process_unmarked_phrase(
        force_str(phrase), inflect_collocation_phrase, *get_forms_tuple(forms))


def plural(phrase, number):
    if not phrase or not number:
        return phrase

    return _process_unmarked_phrase(force_str(phrase), pluralize_phrase, number)

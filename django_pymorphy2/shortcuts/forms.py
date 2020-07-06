from django.utils.encoding import force_str
from django_pymorphy2.constants import INFLECT_FORMS, SPECIFYING_FORMS

__all__ = ['get_forms_tuple']


def get_forms_tuple(*args):
    """
    Converts a string of grammemes to a tuple of two sets:
        - set of tags for declension
        - set of tags for refining the word form
    """
    forms = list()
    specs = list()
    for arg in args:
        for key in force_str(arg).split(','):
            if key in INFLECT_FORMS:
                forms.append(INFLECT_FORMS[key])
            elif key in SPECIFYING_FORMS:
                specs.append(SPECIFYING_FORMS[key])
            else:
                raise ValueError('`%s` is not a grammeme' % key)

    return set(forms), set(specs)

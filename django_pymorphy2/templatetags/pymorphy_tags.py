"""
    Based on
    https://github.com/kmike/pymorphy/blob/master/pymorphy/templatetags/pymorphy_tags.py

"""

from django import template
from django.utils.safestring import mark_safe

from django_pymorphy2 import utils

register = template.Library()


@register.filter
def inflect(phrase, forms):
    phrase = utils.inflect(phrase, forms)
    return mark_safe(phrase)


@register.filter
def inflect_marked(phrase, forms=None):
    phrase = utils.inflect_marked(phrase, forms)
    return mark_safe(phrase)


@register.filter
def inflect_collocation(phrase, forms):
    phrase = utils.inflect_collocation(phrase, forms)
    return mark_safe(phrase)


@register.filter
def plural(phrase, number):
    phrase = utils.plural(phrase, number)
    return mark_safe(phrase)


@register.tag(name='blockinflectmarked')
def block_inflect_marked(parser, token):
    """
    Analizes Russian and English morphology and converts phrases to the
    specified forms.
    Allows to specify the word form in the text inside trans/blocktrans tags.
    Thereby this info can be changed using translation files.
    The phrase "покупайте [[рыбу|вн]]" could be changed to
    "не уходите без [[рыбы|рд]]".

    Template:
    {% blockinflect %}
        {% blocktrans %}
            Buy the {{ product_name }}
        {% endblocktrans %}
    {% endblockinflect %}

    Translation files:
        msgid "Buy the %(product_name)s"
        msgstr "Не уходите без [[%(product_name)s|рд]]"
    """
    nodelist = parser.parse(('endblockinflectmarked',))
    parser.delete_first_token()
    return InflectNode(nodelist)


class InflectNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        output = inflect_marked(output)
        return output


@register.tag(name='blockplural')
def block_plural(parser, token):
    """
    Same as plural filter
    Example:
        {% blockplural amount %}{% trans "Book" %}{% endblockplural %}
    """
    nodelist = parser.parse(('endblockplural',))
    parser.delete_first_token()
    tag_name, amount = token.split_contents()
    return PluralNode(nodelist, amount)


class PluralNode(template.Node):

    def __init__(self, nodelist, amount):
        self.nodelist = nodelist
        self.amount = template.Variable(amount)

    def render(self, context):
        output = self.nodelist.render(context)
        if not output:
            return output

        return plural(output, self.amount.resolve(context))


from django import template

#  Initialize tags
register = template.Library()


@register.filter(name='dict_lookup')
def dict_lookup(dictionary, key):
    """
    Retrives value from dict
    """
    return dictionary.get(key, "")

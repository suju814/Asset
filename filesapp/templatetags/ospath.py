
from os.path import splitext

from django import template


register = template.Library()

@register.filter
def noext(value):
    return splitext(value)[0]
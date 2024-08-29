# KaSheaCosmetics_products/templatetags/custom_filters.py

from django import template

register = template.Library()


@register.filter
def range_filter(value):
    """Returns a range object for a given integer value."""
    try:
        return range(value)
    except TypeError:
        return range(0)


@register.simple_tag
def get_range(value):
    """Returns a range object that can be used in templates."""
    return range(value)

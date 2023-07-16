from pathlib import Path

from django import template

register = template.Library()


@register.filter(is_safe=False)
def file_name(value):
    return Path(value).name
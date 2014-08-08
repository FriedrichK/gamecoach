from django import template
register = template.Library()


@register.filter
def percentage(value):
    if value is None or value == '':
        return None
    return format(value, "0.1%")

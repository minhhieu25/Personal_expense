from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def format_currency(value):
    try:
        return f"{float(value):,.0f} đ"
    except(ValueError, TypeError):
        return value

@register.filter
def split(value, arg):
    return value.split(arg)
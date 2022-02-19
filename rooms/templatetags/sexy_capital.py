from django import template

register = template.Library()


@register.filter()
def sexy_capital(value):
    print(value)
    return value.capitalize()

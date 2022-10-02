from django import template

register = template.Library()


@register.filter(name='dictionairy_keys')
def dictionairy_keys(d, key):
    return d[key]
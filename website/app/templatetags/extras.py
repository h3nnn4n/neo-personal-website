from django import template


register = template.Library()


@register.filter
def underscorize(value):
    return value.replace(" ", "_")

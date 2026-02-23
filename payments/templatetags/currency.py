from django import template

register = template.Library()


@register.filter(name="bgn")
def bgn(value):
    if value in (None, ""):
        return ""
    return f"{value} лв."

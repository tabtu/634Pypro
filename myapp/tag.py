from django import template

register = template.Library()

@register.filter("trimdash")

def trimdash(text):
    return "" if not text else text.replace("-", " ")

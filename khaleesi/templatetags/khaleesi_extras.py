from django import template
register = template.Library()

@register.filter
def ejemplo(obj):
    return 'Ejemplo'

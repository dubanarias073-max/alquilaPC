from django import template

register = template.Library()


@register.filter
def pesos(valor):
    """Formato moneda colombiana: $1.214.500"""
    try:
        return "$" + f"{int(valor):,}".replace(",", ".")
    except (TypeError, ValueError):
        return valor

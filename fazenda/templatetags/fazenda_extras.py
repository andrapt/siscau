from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()

@register.filter(name='currency_brl')
def currency_brl(value):
    """Format a number as Brazilian Real currency, e.g., R$ 1.234,56."""
    if value in (None, ''):
        return 'R$ 0,00'
    try:
        d = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return 'R$ 0,00'
    s = '{:,.2f}'.format(d)
    s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'R$ {s}'
from django import template

register = template.Library()

@register.filter
def get_payment_method_display(value):
    payment_methods = {
        'CASH': 'Cash',
        'CARD': 'Card',
        'MOBILE': 'GCash Payment'
    }
    return payment_methods.get(value, value)

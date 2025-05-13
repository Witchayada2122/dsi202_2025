from django import template

register = template.Library()

@register.filter
def currency(value):
    """แปลงค่าเป็นรูปแบบสกุลเงิน"""
    return f"฿ {value:,.2f}"

@register.filter
def multiply(value, arg):
    """คูณราคากับจำนวนสินค้า"""
    try:
        return value * arg
    except (ValueError, TypeError):
        return value

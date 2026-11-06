from django import template

register = template.Library()


@register.filter
def plural_ru(number, forms):
    try:
        value = abs(int(number))
    except (TypeError, ValueError):
        return ""

    one, few, many = (forms.split(",") + ["", "", ""])[:3]

    if value % 10 == 1 and value % 100 != 11:
        return one
    if 2 <= value % 10 <= 4 and not 12 <= value % 100 <= 14:
        return few
    return many


@register.filter
def num(value, decimals=2):
    try:
        number = float(value)
        digits = int(decimals)
    except (TypeError, ValueError):
        return value

    text = f"{number:.{digits}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")

    return text.replace(".", ",")

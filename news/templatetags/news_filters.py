# news/templatetags/news_filters.py
from django import template
import calendar

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Pozwala na dostęp do elementów słownika w szablonach za pomocą klucza.
    Użycie: {{ my_dict|get_item:key }}
    """
    return dictionary.get(key)

@register.filter(name='month_name')
def month_name(month_number):
    """
    Zwraca polską nazwę miesiąca dla podanego numeru.
    """
    month_names_pl = [
        "", "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
        "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"
    ]
    if 1 <= month_number <= 12:
        return month_names_pl[month_number]
    return ""

@register.filter(name='starts_with')
def starts_with(value, arg):
    """
    Sprawdza, czy string zaczyna się od podanego argumentu.
    Użycie: {{ some_string|starts_with:"prefix" }}
    """
    return value.startswith(arg)
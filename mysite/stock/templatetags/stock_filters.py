from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """딕셔너리에서 키로 값을 조회하는 필터"""
    return dictionary.get(key, [])

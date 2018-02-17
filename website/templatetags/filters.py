from django.template.defaulttags import register


@register.filter
def hash(dictionary, key):
    return dictionary.get(key)

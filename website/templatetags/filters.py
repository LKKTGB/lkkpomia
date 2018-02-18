import os

from bs4 import BeautifulSoup
from django.contrib.staticfiles import finders
from django.template.defaulttags import register
from django.utils.safestring import mark_safe


@register.filter
def hash(dictionary, key):
    return dictionary.get(key)


@register.filter
def svg(filename, size):
    paths = finders.find(os.path.join('svg', '%s.svg' % filename), all=True)
    path = paths[0]
    with open(path) as fp:
        content = fp.read()

    w, h = size.split()
    soup = BeautifulSoup(content, 'html.parser')
    soup.svg['width'] = w
    soup.svg['height'] = h
    return mark_safe(str(soup))

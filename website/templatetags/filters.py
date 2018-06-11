import os

from bs4 import BeautifulSoup
from django.contrib.staticfiles import finders
from django.template.defaulttags import register
from django.utils import timezone
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


@register.filter
def status(event):
    now = timezone.now()

    status_list = []
    if now > event.start_time and now < event.end_time:
        status_list.append('進行中')
    if now > event.registration_start_time and now < event.registration_end_time:
        status_list.append('報名中')
    if hasattr(event, 'videocontest') and \
            now > event.videocontest.voting_start_time and now < event.videocontest.voting_end_time:
        status_list.append('投票中')
    return status_list


@register.filter
def is_registration_open(event):
    now = timezone.now()
    if now > event.registration_start_time and now < event.registration_end_time:
        return True
    else:
        return False


@register.filter
def tags(event):
    if hasattr(event, 'salon'):
        return event.salon.tags.all()
    elif hasattr(event, 'videocontest'):
        return event.videocontest.tags.all()
    return []

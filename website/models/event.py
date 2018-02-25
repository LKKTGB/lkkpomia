from django.db import models
from django.utils.translation import ugettext_lazy as _

from website.models.post import Post


class Event(Post):
    start_time = models.DateTimeField(_('event_start_time'))
    end_time = models.DateTimeField(_('event_end_time'))
    registration_start_time = models.DateTimeField(_('event_registration_start_time'))
    registration_end_time = models.DateTimeField(_('event_registration_end_time'))

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')

from django.db import models
from django.utils.translation import ugettext_lazy as _

from website.models.event import Event


class Announcement(models.Model):
    title = models.CharField(_('announcement_title'), max_length=100)
    body = models.TextField(_('announcement_body'))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name=_('event'))

    create_time = models.DateTimeField(_('announcement_create_time'), auto_now_add=True)
    update_time = models.DateTimeField(_('announcement_update_time'), auto_now=True)

    class Meta:
        verbose_name = _('announcement')
        verbose_name_plural = _('announcements')

from django.db import models
from django.utils.translation import ugettext_lazy as _

from website.models.event import Event


class Salon(Event):
    venue = models.CharField(_('salon_venue'), max_length=100)
    address = models.CharField(_('salon_address'), max_length=100)
    door_time = models.DateTimeField(_('salon_door_time'))

    class Meta:
        verbose_name = _('salon')
        verbose_name_plural = _('salons')

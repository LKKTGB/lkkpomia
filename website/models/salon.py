from django.db import models
from django.utils.translation import ugettext_lazy as _

from website.models.event import Event
from website.models.registration import Registration


class Salon(Event):
    venue = models.CharField(_('salon_venue'), max_length=100)
    address = models.CharField(_('salon_address'), max_length=100)
    door_time = models.DateTimeField(_('salon_door_time'))
    capacity = models.PositiveSmallIntegerField(_('salon_capacity'), default=0)
    need_email = models.BooleanField(_('salon_need_email'), default=False)
    need_phone_number = models.BooleanField(_('salon_need_phone_number'), default=False)

    class Meta:
        verbose_name = _('salon')
        verbose_name_plural = _('salons')

    def full_capacity(self):
        if self.capacity == 0:
            return False
        return Registration.objects.filter(event=self).count() >= self.capacity

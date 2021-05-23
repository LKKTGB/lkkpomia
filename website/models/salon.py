from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from website.models.event import Event
from website.models.salon_registration import SalonRegistration


class Salon(Event):
    venue = models.CharField(_('salon_venue'), max_length=100)
    address = models.CharField(_('salon_address'), max_length=100)
    door_time = models.DateTimeField(_('salon_door_time'))
    capacity = models.PositiveSmallIntegerField(_('salon_capacity'), default=0)
    need_email = models.BooleanField(_('salon_need_email'), default=False)
    need_phone_number = models.BooleanField(_('salon_need_phone_number'), default=False)
    max_attendance_per_registration = models.PositiveSmallIntegerField(_('max_attendance_per_registration'), default=1, validators=[MinValueValidator(limit_value=1)])

    class Meta:
        verbose_name = _('salon')
        verbose_name_plural = _('salons')

    def attendance(self):
        return SalonRegistration.objects.filter(
            event=self).aggregate(attendance=Sum('attendance'))['attendance']

    def full_capacity(self):
        if self.capacity == 0:
            return False
        return self.attendance() >= self.capacity

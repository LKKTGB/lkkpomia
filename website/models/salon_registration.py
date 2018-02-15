from django.utils.translation import ugettext_lazy as _

from website.models.registration import Registration


class SalonRegistration(Registration):

    class Meta:
        verbose_name = _('salon_registration')
        verbose_name_plural = _('salon_registrations')

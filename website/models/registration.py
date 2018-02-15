from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from website.models.event import Event


class Registration(models.Model):
    submitter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('registration_submitter'))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name=_('event'))

    submit_time = models.DateTimeField(_('registration_submit_time'), auto_now_add=True)

    class Meta:
        verbose_name = _('registration')
        verbose_name_plural = _('registrations')

    def __str__(self):
        return '%s - %s' % (self.event.title, self.submitter.username)

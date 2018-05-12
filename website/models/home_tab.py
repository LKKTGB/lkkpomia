from django.db import models
from django.utils.translation import ugettext_lazy as _


class HomeTab(models.Model):
    name = models.CharField(_('home_tab_name'), max_length=100)
    order = models.PositiveSmallIntegerField(_('home_tab_order'))

    class Meta:
        verbose_name = _('home_tab')
        verbose_name_plural = _('home_tabs')

    def __str__(self):
        return self.name

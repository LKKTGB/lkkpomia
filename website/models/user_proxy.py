from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserProxy(User):

    class Meta:
        proxy = True


UserProxy._meta.get_field('is_superuser').verbose_name = _('user_proxy_is_superuser')
UserProxy._meta.get_field('is_superuser').help_text = _('user_proxy_is_superuser_help_text')

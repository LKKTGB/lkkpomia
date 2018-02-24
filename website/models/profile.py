from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from website.models.video_contest_registration import VideoContestRegistration


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.CharField(max_length=100, blank=True)
    voted_videos = models.ManyToManyField(VideoContestRegistration, related_name='voters', blank=True)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return str(self.user)

    def avatar(self):
        return mark_safe('<img src="%s" />' % self.avatar_url)
    avatar.short_description = _('avatar')

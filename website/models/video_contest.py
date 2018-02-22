from django.db import models
from django.utils.translation import ugettext_lazy as _

from website.models.event import Event


class VideoContest(Event):
    voting_start_time = models.DateTimeField(_('video_contest_voting_start_time'))
    voting_end_time = models.DateTimeField(_('video_contest_voting_end_time'))

    class Meta:
        verbose_name = _('video_contest')
        verbose_name_plural = _('video_contests')

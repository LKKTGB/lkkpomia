from django.db import models
from django.utils.translation import ugettext_lazy as _

from website.models.video_contest import VideoContest


class VideoContestGroup(models.Model):
    video_contest = models.ForeignKey(VideoContest, on_delete=models.CASCADE, verbose_name=_('video_contest'))
    name = models.CharField(_('video_contest_group_name'), max_length=100)

    class Meta:
        verbose_name = _('video_contest_group')
        verbose_name_plural = _('video_contest_groups')

        unique_together = ('video_contest', 'name')

    def __str__(self):
        return '%s - %s' % (self.video_contest.title, self.name)

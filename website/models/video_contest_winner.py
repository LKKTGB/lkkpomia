from django.db import models
from django.utils.translation import ugettext_lazy as _

from website.models.video_contest import VideoContest
from website.models.video_contest_registration import VideoContestRegistration


class VideoContestWinner(models.Model):
    video_contest = models.ForeignKey(VideoContest, on_delete=models.CASCADE, verbose_name=_('video_contest'))
    registration = models.ForeignKey(VideoContestRegistration, on_delete=models.CASCADE,
                                     verbose_name=_('video_contest_winner_registration'))
    prize = models.CharField(_('video_contest_winner_prize'), max_length=100)
    order = models.PositiveSmallIntegerField(_('video_contest_winner_order'))

    class Meta:
        verbose_name = _('video_contest_winner')
        verbose_name_plural = _('video_contest_winners')

        unique_together = ('video_contest', 'registration')

    def __str__(self):
        return '%s - %s' % (self.video_contest.title, self.registration.video_title)

from django.utils.translation import ugettext_lazy as _

from website.models.event import Event


class VideoContest(Event):

    class Meta:
        verbose_name = _('video_contest')
        verbose_name_plural = _('video_contests')

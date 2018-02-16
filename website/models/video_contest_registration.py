from django.db import models
from django.utils.translation import ugettext_lazy as _
from embed_video.fields import EmbedVideoField

from website.models.registration import Registration
from website.models.video_contest_group import VideoContestGroup


class VideoContestRegistration(Registration):
    contestant_name = models.CharField(_('video_contest_registration_contestant_name'), max_length=100)
    phone_number = models.CharField(_('video_contest_registration_phone_number'), max_length=20)
    address = models.CharField(_('video_contest_registration_address'), max_length=100)
    email = models.EmailField(_('video_contest_registration_email'))
    video_title = models.CharField(_('video_contest_registration_video_title'), max_length=100)
    introduction = models.TextField(_('video_contest_registration_introduction'))
    youtube_url = EmbedVideoField(_('video_contest_registration_youtube_url'))
    group = models.ForeignKey(VideoContestGroup, on_delete=models.CASCADE,
                              verbose_name=_('video_contest_registration_group'))
    questions = models.TextField(_('video_contest_registration_questions'), blank=True)

    qualified = models.BooleanField(_('video_contest_registration_qualified'), default=False)

    class Meta:
        verbose_name = _('video_contest_registration')
        verbose_name_plural = _('video_contest_registrations')


VideoContestRegistration._meta.get_field('submitter').verbose_name = _('video_contest_registration_submitter')

from django.db import models
from django.utils.translation import ugettext_lazy as _
from embed_video.fields import EmbedVideoField

from website.models.registration import Registration


class VideoContestRegistration(Registration):
    youtube_url = EmbedVideoField(_('video_contest_registration_youtube_url'))
    introduction = models.TextField(_('video_contest_registration_introduction'))
    phone_number = models.CharField(_('video_contest_registration_phone_number'), max_length=20)
    address = models.CharField(_('video_contest_registration_address'), max_length=100)
    email = models.CharField(_('video_contest_registration_email'), max_length=100)
    questions = models.TextField(_('video_contest_registration_questions'), blank=True)

    qualified = models.BooleanField(_('video_contest_registration_qualified'), default=False)

    class Meta:
        verbose_name = _('video_contest_registration')
        verbose_name_plural = _('video_contest_registrations')


VideoContestRegistration._meta.get_field('submitter').verbose_name = _('video_contest_registration_submitter')

from django import forms
from django.utils.translation import ugettext_lazy as _

from website.models.video_contest_group import VideoContestGroup
from website.models.video_contest_registration import VideoContestRegistration


class VideoContestRegistrationForm(forms.ModelForm):

    class Meta:
        model = VideoContestRegistration
        exclude = (
            'submitter',
            'event',
            'qualified',
        )
        labels = {
            'contestant_name': _('video_contest_registration_form_contestant_name_label'),
        }
        help_texts = {
            'contestant_name': _('video_contest_registration_form_contestant_name_help_text'),
            'address': _('video_contest_registration_form_address_help_text'),
            'email': _('video_contest_registration_form_email_help_text'),
            'video_title': _('video_contest_registration_form_video_title_help_text'),
            'introduction': _('video_contest_registration_form_introduction_help_text'),
            'youtube_url': _('video_contest_registration_form_youtube_url_help_text'),
            'questions': _('video_contest_registration_form_questions_help_text'),
        }
        error_messages = {
            'youtube_url': {
                'unique': _('video_contest_registration_form_youtube_url_error_messages_unique')
            }
        }

    def __init__(self, video_contest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].widget = forms.RadioSelect()
        self.fields['group'].choices = [(g.id, g.name)
                                        for g in VideoContestGroup.objects.filter(video_contest=video_contest)]

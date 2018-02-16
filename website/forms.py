from django import forms
from django.utils.translation import ugettext_lazy as _

from website.models.video_contest_group import VideoContestGroup


class VideoContestRegistrationForm(forms.Form):
    contestant_name = forms.CharField(
        label=_('video_contest_registration_form_contestant_name_label'),
        help_text=_('video_contest_registration_form_contestant_name_help_text'))
    phone_number = forms.CharField(
        label=_('video_contest_registration_form_phone_number_label'))
    address = forms.CharField(
        label=_('video_contest_registration_form_address_label'),
        help_text=_('video_contest_registration_form_address_help_text'))
    email = forms.EmailField(
        label=_('video_contest_registration_form_email_label'),
        help_text=_('video_contest_registration_form_email_help_text'))
    video_title = forms.CharField(
        label=_('video_contest_registration_form_video_title_label'),
        help_text=_('video_contest_registration_form_video_title_help_text'))
    introduction = forms.CharField(
        widget=forms.Textarea(),
        label=_('video_contest_registration_form_introduction_label'),
        help_text=_('video_contest_registration_form_introduction_help_text'))
    youtube_url = forms.URLField(
        label=_('video_contest_registration_form_youtube_url_label'),
        help_text=_('video_contest_registration_form_youtube_url_help_text'))
    group = forms.ChoiceField(
        widget=forms.RadioSelect(),
        label=_('video_contest_registration_form_group_label'))
    questions = forms.CharField(
        widget=forms.Textarea(),
        label=_('video_contest_registration_form_questions_label'),
        help_text=_('video_contest_registration_form_questions_help_text'))

    def __init__(self, video_contest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].choices = [(g.id, g.name)
                                        for g in VideoContestGroup.objects.filter(video_contest=video_contest)]

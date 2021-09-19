from django import forms
from django.forms.widgets import HiddenInput
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from website import models


class DeleteForm(forms.Form):

    method = forms.ChoiceField(choices=[(m, m) for m in ('DELETE',)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['method'].initial = 'DELETE'
        self.fields['method'].widget = HiddenInput()


class VideoContestRegistrationForm(forms.ModelForm):

    class Meta:
        model = models.VideoContestRegistration
        exclude = (
            'submitter',
            'qualified',
            'votes',
            'video_number',
        )
        widgets = {
            'event': forms.HiddenInput()
        }
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
        self.video_contest = video_contest
        self.fields['group'].widget = forms.RadioSelect()
        self.fields['group'].choices = [(g.id, g.name)
                                        for g in models.VideoContestGroup.objects.filter(video_contest=video_contest)]

    def clean(self):
        super().clean()

        now = timezone.now()
        if now < self.video_contest.registration_start_time:
            raise forms.ValidationError(
                '%s 開放報名' % self.video_contest.registration_start_time.strftime('%Y/%m/%d %H:%M')
            )
        elif now > self.video_contest.registration_end_time:
            raise forms.ValidationError(
                '已截止報名'
            )


class VideoContestVoteForm(forms.Form):
    method = forms.ChoiceField(choices=[(m, m) for m in ('POST', 'DELETE')])
    video_contest_registration_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['method'].widget = HiddenInput()
        self.fields['video_contest_registration_id'].widget = HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        video_contest_registration_id = cleaned_data.get('video_contest_registration_id')
        video_contset_registration = models.VideoContestRegistration.objects.get(id=video_contest_registration_id)
        video_contest = models.VideoContest.objects.get(id=video_contset_registration.event.id)

        now = timezone.now()
        if now < video_contest.voting_start_time:
            raise forms.ValidationError(
                '%s 開放投票' % video_contest.voting_start_time.strftime('%Y/%m/%d %H:%M')
            )
        elif now > video_contest.voting_end_time:
            raise forms.ValidationError(
                '已截止投票'
            )


class SalonRegistrationForm(forms.ModelForm):

    class Meta:
        model = models.SalonRegistration
        exclude = (
            'event',
            'submitter',
        )
        labels = {
            'contestant_name': _('salon_registration_form_contestant_name_label'),
        }
        help_texts = {
            'contestant_name': _('salon_registration_form_contestant_name_help_text'),
            'email': _('salon_registration_form_email_help_text'),
            'phone_number': _('salon_registration_form_phone_number_help_text'),
        }

    def __init__(self, salon, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.salon = salon
        self.fields['email'].required = salon.need_email
        self.fields['phone_number'].required = salon.need_phone_number

        for field_name in ['email', 'phone_number']:
            if not self.fields[field_name].required:
                self.fields[field_name].label += '（選填）'

        if salon.max_attendance_per_registration == 1:
            self.fields['attendance'].widget = HiddenInput()
            self.fields['other_attendees_info'].widget = HiddenInput()
        else:
            self.fields['attendance'].label += '（最多 %s 人）' % salon.max_attendance_per_registration
            self.fields['other_attendees_info'].label += '（若總出席人數超過 1 人則必填）'

    def clean(self):
        super().clean()

        if self.cleaned_data['attendance'] > self.salon.max_attendance_per_registration:
            raise forms.ValidationError(
                '總出席人數最多 %s 人' % self.salon.max_attendance_per_registration
            )
        if self.salon.capacity > 0 and self.cleaned_data['attendance'] + self.salon.attendance() > self.salon.capacity:
            raise forms.ValidationError(
                '超過活動名額，只能再報名 %s 人' % (self.salon.capacity - self.salon.attendance())
            )
        if self.cleaned_data['attendance'] > 1 and not self.cleaned_data['other_attendees_info']:
            raise forms.ValidationError(
                '請填入其他出席者姓名'
            )

        now = timezone.now()
        if now < self.salon.registration_start_time:
            raise forms.ValidationError(
                '%s 開放報名' % self.salon.registration_start_time.strftime('%Y/%m/%d %H:%M')
            )
        elif now > self.salon.registration_end_time:
            raise forms.ValidationError(
                '已截止報名'
            )
        elif self.salon.full_capacity():
            raise forms.ValidationError(
                '名額已滿'
            )

from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from embed_video.admin import AdminVideoWidget, AdminVideoMixin
from embed_video.fields import EmbedVideoField


class AdminVideoTextInputWidget(AdminTextInputWidget, AdminVideoWidget):
    pass


class AdminVideoTextInputMixin(AdminVideoMixin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, EmbedVideoField):
            return db_field.formfield(widget=AdminVideoTextInputWidget)

        return super(AdminVideoMixin, self).formfield_for_dbfield(db_field, **kwargs)


class VideoContestRegistrationAdmin(AdminVideoTextInputMixin, admin.ModelAdmin):
    list_display = ('event', 'group', 'video_number', 'qualified', 'video_title', 'contestant_name', 'votes')
    list_filter = ('event', 'qualified')

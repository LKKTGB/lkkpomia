from django.contrib import admin

from website.models.video_contest_group import VideoContestGroup


class VideoContestGroupInline(admin.StackedInline):
    model = VideoContestGroup

    extra = 0
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class VideoContestAdmin(admin.ModelAdmin):
    inlines = [
        VideoContestGroupInline,
    ]

    class Media:
        js = [
            'js/tinymce/tinymce.min.js',
            'js/tinymce_settings.js',
        ]

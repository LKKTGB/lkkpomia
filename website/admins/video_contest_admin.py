from django.contrib import admin
from django.urls import resolve

from website import models


class VideoContestGroupInline(admin.StackedInline):
    model = models.VideoContestGroup

    extra = 0
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class VideoContestWinnerInline(admin.StackedInline):
    model = models.VideoContestWinner

    extra = 0
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

    def get_parent_object_from_request(self, request):
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.get(pk=resolved.kwargs['object_id'])
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        video_contest = self.get_parent_object_from_request(request)
        if db_field.name == 'registration' and video_contest:
            kwargs['queryset'] = models.VideoContestRegistration.objects.filter(event=video_contest.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class VideoContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time')

    inlines = [
        VideoContestGroupInline,
        VideoContestWinnerInline,
    ]

    class Media:
        js = [
            'js/tinymce/tinymce.min.js',
            'js/tinymce_settings.js',
        ]

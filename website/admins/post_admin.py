from django.contrib import admin


class PostAdmin(admin.ModelAdmin):

    class Media:
        js = [
            'js/tinymce/tinymce.min.js',
            'js/tinymce_settings.js',
        ]

    def has_add_permission(self, request):
        return False

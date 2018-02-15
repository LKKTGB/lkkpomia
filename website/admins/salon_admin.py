from django.contrib import admin


class SalonAdmin(admin.ModelAdmin):

    class Media:
        js = [
            'js/tinymce/tinymce.min.js',
            'js/tinymce_settings.js',
        ]

from django.contrib import admin


class HomeTabAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')

    class Media:
        js = [
            'js/tinymce/tinymce.min.js',
            'js/tinymce_settings.js',
        ]

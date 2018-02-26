from solo.admin import SingletonModelAdmin


class PrivacyPolicyAdmin(SingletonModelAdmin):

    class Media:
        js = [
            'js/tinymce/tinymce.min.js',
            'js/tinymce_settings.js',
        ]

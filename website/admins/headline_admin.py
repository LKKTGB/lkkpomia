from django.contrib import admin


class HeadlineAdmin(admin.ModelAdmin):
    list_display = ('post', 'start_time', 'end_time')

    raw_id_fields = ('post',)
    autocomplete_lookup_fields = {
        'fk': ['post']
    }

from django.contrib import admin


class SalonRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event',
                    'contestant_name', 'phone_number', 'email', 'attendance',
                    'submitter_full_name', 'submit_time')
    list_filter = ('event',)

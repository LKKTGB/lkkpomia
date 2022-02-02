from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from website import models


class SalonAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'venue', 'checkin_table')

    def checkin_table(self, obj):
        return mark_safe('<a href="%s">簽到表</a>' % reverse('admin:salon_attendees', kwargs={'object_id': obj.id}))
    checkin_table.short_description = '簽到表'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/attendees/', self.attendees, name='salon_attendees'),
        ]
        return custom_urls + urls

    def attendees(self, request, object_id):
        salon = models.Salon.objects.get(id=object_id)
        registrations = models.SalonRegistration.objects.filter(event=salon)
        return TemplateResponse(request, 'admin/salon/attendees.html', {
            'salon': salon,
            'registrations': registrations
        })

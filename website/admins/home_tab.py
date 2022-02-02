from django.contrib import admin


class HomeTabAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')

from django.contrib import admin


class PostAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

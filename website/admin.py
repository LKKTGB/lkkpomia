from django.contrib import admin
from django.contrib.auth.models import User

from website.admins.user_profile_admin import UserProfileAdmin


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)

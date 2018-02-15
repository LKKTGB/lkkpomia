from django.contrib import admin
from django.contrib.auth.models import User

from website.admins.post_admin import PostAdmin
from website.admins.user_profile_admin import UserProfileAdmin
from website.models.post import Post

admin.site.unregister(User)
admin.site.register(Post, PostAdmin)
admin.site.register(User, UserProfileAdmin)

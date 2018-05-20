from django.contrib import admin
from django.contrib.auth.models import Group, User
from social_django.models import Association, Nonce, UserSocialAuth
from taggit.admin import Tag

from website import models
from website import admins

admin.site.unregister(Association)
admin.site.unregister(Group)
admin.site.unregister(Nonce)
admin.site.unregister(Tag)
admin.site.unregister(User)
admin.site.unregister(UserSocialAuth)
# admin.site.register(models.Announcement, admins.AnnouncementAdmin)
# admin.site.register(models.Event, admins.EventAdmin)
admin.site.register(models.Headline, admins.HeadlineAdmin)
admin.site.register(models.HomeTab, admins.HomeTabAdmin)
admin.site.register(models.Post, admins.PostAdmin)
admin.site.register(models.PrivacyPolicy, admins.PrivacyPolicyAdmin)
admin.site.register(models.Salon, admins.SalonAdmin)
admin.site.register(models.SalonRegistration, admins.SalonRegistrationAdmin)
admin.site.register(models.UserProxy, admins.UserProfileAdmin)
admin.site.register(models.VideoContest, admins.VideoContestAdmin)
admin.site.register(models.VideoContestRegistration, admins.VideoContestRegistrationAdmin)

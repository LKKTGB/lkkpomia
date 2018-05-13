from django.contrib import admin
from django.contrib.auth.models import Group, User
from social_django.models import Association, Nonce, UserSocialAuth
from taggit.admin import Tag

from website import models
from website.admins.announcement_admin import AnnouncementAdmin
from website.admins.event_admin import EventAdmin
from website.admins.home_tab import HomeTabAdmin
from website.admins.post_admin import PostAdmin
from website.admins.privacy_policy_admin import PrivacyPolicyAdmin
from website.admins.salon_admin import SalonAdmin
from website.admins.salon_registration_admin import SalonRegistrationAdmin
from website.admins.user_profile_admin import UserProfileAdmin
from website.admins.video_contest_admin import VideoContestAdmin
from website.admins.video_contest_registration_admin import VideoContestRegistrationAdmin

admin.site.unregister(Association)
admin.site.unregister(Group)
admin.site.unregister(Nonce)
admin.site.unregister(Tag)
admin.site.unregister(User)
admin.site.unregister(UserSocialAuth)
# admin.site.register(models.Announcement, AnnouncementAdmin)
# admin.site.register(models.Event, EventAdmin)
admin.site.register(models.HomeTab, HomeTabAdmin)
# admin.site.register(models.Post, PostAdmin)
admin.site.register(models.PrivacyPolicy, PrivacyPolicyAdmin)
admin.site.register(models.Salon, SalonAdmin)
# admin.site.register(models.SalonRegistration, SalonRegistrationAdmin)
admin.site.register(models.UserProxy, UserProfileAdmin)
admin.site.register(models.VideoContest, VideoContestAdmin)
admin.site.register(models.VideoContestRegistration, VideoContestRegistrationAdmin)

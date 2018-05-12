from django.contrib import admin
from django.contrib.auth.models import Group, User
from social_django.models import Association, Nonce, UserSocialAuth
from taggit.admin import Tag

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
from website.models.announcement import Announcement
from website.models.event import Event
from website.models.home_tab import HomeTab
from website.models.post import Post
from website.models.privacy_policy import PrivacyPolicy
from website.models.salon import Salon
from website.models.salon_registration import SalonRegistration
from website.models.user_proxy import UserProxy
from website.models.video_contest import VideoContest
from website.models.video_contest_registration import VideoContestRegistration

admin.site.unregister(Association)
admin.site.unregister(Group)
admin.site.unregister(Nonce)
admin.site.unregister(Tag)
admin.site.unregister(User)
admin.site.unregister(UserSocialAuth)
# admin.site.register(Announcement, AnnouncementAdmin)
# admin.site.register(Event, EventAdmin)
admin.site.register(HomeTab, HomeTabAdmin)
# admin.site.register(Post, PostAdmin)
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
# admin.site.register(Salon, SalonAdmin)
# admin.site.register(SalonRegistration, SalonRegistrationAdmin)
admin.site.register(UserProxy, UserProfileAdmin)
admin.site.register(VideoContest, VideoContestAdmin)
admin.site.register(VideoContestRegistration, VideoContestRegistrationAdmin)

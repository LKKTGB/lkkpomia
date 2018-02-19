from django.contrib.auth.models import User
from django.db import models

from website.models.video_contest_registration import VideoContestRegistration


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.CharField(max_length=100, blank=True)
    voted_videos = models.ManyToManyField(VideoContestRegistration, related_name='+')

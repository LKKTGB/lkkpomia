from django.contrib.auth.models import User
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver

from website.models.profile import Profile
from website.models.video_contest_registration import VideoContestRegistration


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=VideoContestRegistration)
def generate_video_number_after_qualified(sender, instance, **kwargs):
    if not instance.qualified:
        return
    if instance.video_number:
        return
    next_number = VideoContestRegistration.objects.all().aggregate(Max('video_number'))['video_number__max'] + 1
    instance.video_number = next_number
    instance.save()

from django.contrib.auth.models import User
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver

from website import models


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=models.UserProxy)
def add_permission_to_superuser(sender, instance, **kwargs):
    if instance.is_staff != instance.is_superuser:
        instance.is_staff = instance.is_superuser
        instance.save()


@receiver(post_save, sender=models.VideoContestRegistration)
def generate_video_number_after_qualified(sender, instance, **kwargs):
    if not instance.qualified:
        return
    if instance.video_number:
        return
    last_number = models.VideoContestRegistration.objects.all().aggregate(Max('video_number'))['video_number__max'] or 0
    instance.video_number = last_number + 1
    instance.save()

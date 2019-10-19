from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import FacultyProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = FacultyProfile.objects.create(faculty=instance)
        profile.save()
@receiver(post_save, sender=FacultyProfile)
def save_profile(sender, instance, **kwargs):
    pass

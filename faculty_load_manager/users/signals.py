from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *
from load_manager.models import *

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = FacultyProfile.objects.create(faculty=instance)
        u = UserProfile.objects.create(user=instance)
        profile.save()
        u.save()
# @receiver(post_save, sender=Setting)
# def create_SemesterOffering(sender, instance, created, **kwargs):
#     if created:
#         semester_offering = SemesterOffering()
#         semester_offering.school_year = instance.school_year
#         semester_offering.semester = instance.semester
#
#         os.system("cls")
#
#         # semester_offering.save()

@receiver(post_save, sender=FacultyProfile)
def save_profile(sender, instance, **kwargs):
    pass

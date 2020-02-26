from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *
#


@receiver(post_save, sender=BlockSection)
def save_profile(sender, instance, **kwargs):
    pass

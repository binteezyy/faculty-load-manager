from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import *
from .views import randomPassword
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:

        try:
            if instance.is_superuser or instance.is_staff:
                message = f'Hi {instance.first_name}! You have been registered as a staff account,contact your site admin for the password'
            else:
                r = randomPassword()
                instance.set_password(r)
                message = f'Hi {instance.first_name}! You have been registered. Here is your temporary password:  {r}'
            profile = FacultyProfile.objects.create(faculty=instance)
            user_profile = UserProfile.objects.create(user=instance)
            profile.save()
            user_profile.save()
            instance.save()

            subject = 'Welcome to Computer Engineering Faculty Website'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [instance.email,]
            send_mail( subject, message, email_from, recipient_list )

        except Exception as e:
            instance.delete()
            raise e

@receiver(post_save, sender=FacultyProfile)
def save_profile(sender, instance, **kwargs):
    pass

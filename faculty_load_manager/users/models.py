from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.conf import settings


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


class TimeSelect(models.Model):
    DAY_OF_THE_WEEK = [
     (0, 'MONDAY'),
     (1, 'TUESDAY'),
     (2, 'WEDNESDAY'),
     (3, 'THURSDAY'),
     (4, 'FRIDAY'),
     (5, 'SATURDAY'),
     (6, 'SUNDAY')
    ]
    TIME_SELECT = [
    (0, '07:30-08:00'),     (1, '08:00-08:30'),     (2, '08:30-09:00'),
    (3, '09:00-09:30'),     (4, '09:30-10:00'),     (5, '10:00-10:30'),
    (6, '10:30-11:00'),     (7, '11:00-11:30'),     (8, '11:30-12:00'),
    (9, '12:00-12:30'),     (10, '12:30-13:00'),    (11, '13:00-13:30'),
    (12, '13:30-14:00'),    (13, '14:00-14:30'),    (14, '14:30-15:00'),
    (15, '15:00-15:30'),    (16, '15:30-16:00'),    (17, '16:00-16:30'),
    (18, '16:30-17:00'),    (19, '17:00-17:30'),    (20, '17:30-18:00'),
    (21, '18:00-18:30'),    (22, '18:30-19:00'),    (23, '19:00-19:30'),
    (24, '19:30-20:00'),    (25, '20:00-20:30'),    (26, '20:30-21:00'),
    ]

    select_time = models.IntegerField(choices = TIME_SELECT, default = 0)
    select_day = models.IntegerField(choices = DAY_OF_THE_WEEK, default = 0)
    class Meta:
        unique_together = ('select_time','select_day')
    def __str__(self):
        return f'{self.get_select_day_display()} — {self.get_select_time_display()}'

class PreferredSchedule(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    preferred_time = models.ManyToManyField(TimeSelect)
    created_at = models.DateTimeField(auto_now_add=True , null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

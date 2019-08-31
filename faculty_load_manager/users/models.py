from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.conf import settings

from load_manager.models import *

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

class Setting(models.Model):
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, null = True)
    semester = models.IntegerField(choices = SEMESTERS(), default = 0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ],
    null = True)

    def __str__(self):
        return f'SETTINGS'

    def save(self, *args, **kwargs):
        save_permission = Setting.has_add_permission(self)
        self.id = 1
        if Setting.objects.all().count() < 1:
            super(Setting, self).save()
        elif save_permission:
            super(Setting, self).save()


    def has_add_permission(self):
        return Setting.objects.filter(id=self.id).exists()

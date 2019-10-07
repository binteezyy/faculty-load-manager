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
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.CASCADE, null=True)
    semester = models.IntegerField(choices=SEMESTERS(), default=0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ],
        null=True)
    first_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, null=True, related_name='first_year_curriculum')
    second_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, null=True, related_name='second_year_curriculum')
    third_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, null=True, related_name='third_year_curriculum')
    fourth_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, null=True, related_name='fourth_year_curriculum')
    fifth_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, null=True, related_name='fifth_year_curriculum')
    first_sections = models.PositiveIntegerField(default=0)
    second_sections = models.PositiveIntegerField(default=0)
    third_sections = models.PositiveIntegerField(default=0)
    fourth_sections = models.PositiveIntegerField(default=0)
    fifth_sections = models.PositiveIntegerField(default=0)



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


class FacultyProfile(models.Model):
    F_TYPE = [
        (0, 'Part-time'),
        (1, 'Regular'),
        (2, 'Chief'),
        (3, 'Director')
    ]

    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    faculty_type = models.IntegerField(choices=F_TYPE, default=1)
    regular_hours = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])
    part_time_hours = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.faculty} {self.get_faculty_type_display()}'

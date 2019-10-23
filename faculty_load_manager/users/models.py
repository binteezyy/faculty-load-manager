from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from django.conf import settings

from load_manager.models import *

from PIL                                        import Image
def SEMESTER_STATUS():
    return [(0, 'Not Opened'),
              (1, 'Open'),
              (2, 'Closed'),
              (3, 'Locked')]


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

class AnnouncementCategory(models.Model):
    category = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.category}'

class Announcements(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(AnnouncementCategory, on_delete=models.CASCADE)
    message = models.TextField()
    author = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'
class Setting(models.Model):
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.CASCADE, null=True)
    semester = models.IntegerField(choices=SEMESTERS(), default=0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ],
        null=True)
    first_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, null=True,blank=True, related_name='first_year_curriculum')
    second_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, null=True, blank=True, related_name='second_year_curriculum')
    third_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, null=True, blank=True, related_name='third_year_curriculum')
    fourth_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, null=True, blank=True, related_name='fourth_year_curriculum')
    fifth_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, null=True, blank=True, related_name='fifth_year_curriculum')
    first_sections = models.PositiveIntegerField(default=0)
    second_sections = models.PositiveIntegerField(default=0)
    third_sections = models.PositiveIntegerField(default=0)
    fourth_sections = models.PositiveIntegerField(default=0)
    fifth_sections = models.PositiveIntegerField(default=0)

    current = models.BooleanField(default=False)

    status = models.IntegerField(choices = SEMESTER_STATUS(), default = 0, validators=[
        MaxValueValidator(3),
        MinValueValidator(0)
    ])

    class Meta:
        unique_together = ('school_year', 'semester')

    def __str__(self):
        return f'[{self.school_year}] {self.get_semester_display()}'

    def save(self, *args, **kwargs):
        if self.current:
            try:
                temp = Setting.objects.get(current=True)
                if self != temp:
                    temp.current = False
                    temp.save()
            except Setting.DoesNotExist:
                pass
        super(Setting, self).save(*args, **kwargs)

    # def delete(self):
    #     if self.current == True:
    #         raise ValueError('You cannot delete current')
    #     else:
    #         super(Setting, self).delete()

class UserProfile(models.Model):
    user   = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics',null=True, blank=True)

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

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

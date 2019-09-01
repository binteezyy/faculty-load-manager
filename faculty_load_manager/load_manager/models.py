from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.conf import settings

# ==================== SELECT FUNCTIONS ||
def DAY_OF_THE_WEEK():
    return [
     (0, 'MONDAY'),
     (1, 'TUESDAY'),
     (2, 'WEDNESDAY'),
     (3, 'THURSDAY'),
     (4, 'FRIDAY'),
     (5, 'SATURDAY'),
     (6, 'SUNDAY')
    ]
def SEMESTERS():
    return [
     (0, 'FIRST SEMESTER'),
     (1, 'SECOND SEMESTER'),
     (2, 'SUMMER')
    ]

# ==================== MAIN ||
class Year(models.Model):
    import datetime
    current_year = datetime.date.today().year
    year = models.IntegerField(default=current_year, validators=[MinValueValidator(0), MaxValueValidator(current_year + 5)],unique=True)

    def __str__(self):
        return f'{self.year}'

class Curriculum(models.Model):
    curriculum = models.CharField(max_length=56)
    description = models.CharField(max_length=128, blank=True)
    def __str__(self):
        return f'{self.curriculum}'

class Subject(models.Model):
    year_level = models.PositiveIntegerField(default=1,
    validators=[
    MaxValueValidator(6),
    MinValueValidator(1)
    ]
    )
    semester = models.IntegerField(choices = SEMESTERS(), default = 0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ])
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=15)
    subject_name = models.CharField(max_length=128)
    minor_flag = models.BooleanField(default=False)
    thesis_flag = models.BooleanField(default=False)
    ojt_flag = models.BooleanField(default=False)
    lab_hours = models.PositiveIntegerField(default=0)
    lec_hours = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.subject_name}'

    class Meta:
        ordering=['year_level', 'semester']
        unique_together = ('subject_code', 'subject_name')

class SchoolYear(models.Model):
    start_year = models.ForeignKey(Year,on_delete=models.CASCADE, related_name='startyear')
    end_year = models.ForeignKey(Year,on_delete=models.CASCADE, related_name='endyear')

    class Meta:
        unique_together = ('start_year','end_year')
        
    def __str__(self):
        return f'{self.start_year} — {self.end_year}'

class BlockSection(models.Model):
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    semester = models.IntegerField(choices = SEMESTERS(), default = 0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ])
    year_level = models.PositiveIntegerField(default = 1,validators=[MinValueValidator(1)])
    section = models.CharField(max_length=56)
    
    class Meta:
        unique_together = ('school_year','semester','year_level','section')

    def __str__(self):
        if self.name:
            return f'{self.name}'
        else:
            return f'{self.year_level} - {self.section}'

class SemesterOffering(models.Model):
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    semester = models.IntegerField(choices = SEMESTERS(), default = 0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ])
    subject = models.ManyToManyField(Subject)

    class Meta:
        unique_together = ('school_year','semester')

    def __str__(self):
        return f'[{self.school_year}]  {self.get_semester_display()}'

class Room(models.Model):
    ROOM_CAT = [
        (0, 'Lab'),
        (1, 'Lecture'),
    ]
    room_name = models.CharField(max_length=15)
    room_category = models.IntegerField(choices = ROOM_CAT, default=1)

    def __str__(self):
        return f'{self.room_name} - {self.get_room_category_display()}'

class SectionOffering(models.Model):
    SERVICE = [
    (0, 'From Curriculum'),
    (1, 'Service Subject'),
    (2, 'Petition'),
    (3, 'Tutorial'),
    ]

    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    semester = models.IntegerField(choices = SEMESTERS(), default = 0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ])
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    block_section = models.ForeignKey(BlockSection, on_delete=models.CASCADE)
    day = models.IntegerField(choices = DAY_OF_THE_WEEK(), default = 0)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    service_flag = models.IntegerField(choices = SERVICE, default = 0)

    def __str__(self):
        return f'{self.subject}'

class PreferredTime(models.Model):
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
    select_day = models.IntegerField(choices = DAY_OF_THE_WEEK(), default = 0)

    class Meta:
        unique_together = ('select_time','select_day')

    def __str__(self):
        return f'{self.get_select_day_display()} — {self.get_select_time_display()}'

class PreferredSchedule(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    preferred_subject = models.ManyToManyField(Subject)
    preferred_time = models.ManyToManyField(PreferredTime)
    created_at = models.DateTimeField(auto_now_add=True , null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)



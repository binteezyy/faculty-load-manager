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
    year = models.IntegerField(default=current_year, validators=[
                               MinValueValidator(0), MaxValueValidator(current_year + 5)], unique=True)

    def __str__(self):
        return f'{self.year}'


class Curriculum(models.Model):
    curriculum = models.CharField(max_length=56, unique=True)
    description = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f'Curriculum {self.curriculum}'


class Subject(models.Model):
    year_level = models.PositiveIntegerField(default=1,
                                             validators=[
                                                 MaxValueValidator(6),
                                                 MinValueValidator(1)
                                             ]
                                             )
    semester = models.IntegerField(choices=SEMESTERS(), default=0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ])
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=15)
    subject_name = models.CharField(max_length=128)
    offered = models.BooleanField(default=False)
    lab_hours = models.PositiveIntegerField(default=0)
    lec_hours = models.PositiveIntegerField(default=0)

    ROOM_CAT = [
        (0, 'Lab'),
        (1, 'Lecture'),
        (2, 'Electronics Lab'),
    ]

    room_category = models.IntegerField(choices=ROOM_CAT, default=1)

    def __str__(self):
        return f'{self.subject_code}: {self.subject_name}'

    class Meta:
        ordering = ['year_level', 'semester']
        unique_together = ('subject_code', 'subject_name')


class SchoolYear(models.Model):
    start_year = models.ForeignKey(
        Year, on_delete=models.CASCADE, related_name='startyear')
    end_year = models.ForeignKey(
        Year, on_delete=models.CASCADE, related_name='endyear')

    class Meta:
        unique_together = ('start_year', 'end_year')

    def __str__(self):
        return f'{self.start_year} — {self.end_year}'


class BlockSection(models.Model):
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=SEMESTERS(), default=0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ])
    year_level = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])
    section = models.CharField(max_length=56)

    class Meta:
        unique_together = ('school_year', 'semester', 'year_level', 'section')
        ordering = ['school_year', 'semester', 'year_level', 'section']

    def __str__(self):
        return f'{self.year_level} - {self.section} | {self.school_year} - {self.get_semester_display()}'


class SemesterOffering(models.Model):
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=SEMESTERS(), default=0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ])
    subject = models.ManyToManyField(Subject)

    class Meta:
        unique_together = ('school_year', 'semester')

    def __str__(self):
        return f'[{self.school_year}]  {self.get_semester_display()}'


class Room(models.Model):
    ROOM_CAT = [
        (0, 'Lab'),
        (1, 'Lecture'),
        (2, 'Electronics Lab'),
    ]
    room_name = models.CharField(max_length=15)
    room_category = models.IntegerField(choices=ROOM_CAT, default=1)

    def __str__(self):
        return f'{self.room_name} - {self.get_room_category_display()}'

    class Meta:
        unique_together = ('room_name', 'room_category')


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
        null=True, blank=True
    )

    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=SEMESTERS(), default=0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ])
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    block_section = models.ForeignKey(BlockSection, on_delete=models.CASCADE)
    service_flag = models.IntegerField(choices=SERVICE, default=0)

    def __str__(self):
        return f'{self.subject} - {self.professor} - {self.block_section}'

    class Meta:
        unique_together = ('school_year', 'semester',
                           'subject', 'block_section', 'service_flag')


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

    select_time = models.IntegerField(choices=TIME_SELECT, default=0)
    select_day = models.IntegerField(choices=DAY_OF_THE_WEEK(), default=0)

    class Meta:
        unique_together = ('select_time', 'select_day')

    def __str__(self):
        return f'{self.get_select_day_display()} — {self.get_select_time_display()}'


class LoadSchedule(models.Model):
    preferred_time = models.ManyToManyField(PreferredTime, blank=True)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.room} - {self.preferred_time.all().first()} to {self.preferred_time.all().last()}'


class FacultyLoad(models.Model):
    LOAD_CAT = [
        (0, 'Lab 1'),
        (1, 'Lab 2'),
        (2, 'Lec 1'),
        (3, 'Lec 2'),
    ]

    load_schedule = models.ForeignKey(
        LoadSchedule, on_delete=models.CASCADE, blank=True, null=True)
    load_category = models.IntegerField(choices=LOAD_CAT, default=1)
    subject = models.ForeignKey(SectionOffering, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_load_category_display()} - {self.subject.subject.subject_name} - {self.load_schedule}'

    class Meta:
        unique_together = ('load_category', 'subject')


class PreferredSchedule(models.Model):
    STATUS = [
        (0, 'To be reviewed'),
        (1, 'Processed'),
        (2, 'Locked'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status = models.IntegerField(choices=STATUS, default=0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ])
    preferred_subject = models.ManyToManyField(Subject)
    preferred_time = models.ManyToManyField(PreferredTime)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=SEMESTERS(), default=0, validators=[
        MaxValueValidator(2),
        MinValueValidator(0)
    ])
    is_editable = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'school_year', 'semester')

    def __str__(self):
        return f'{self.user.username} PLOAD{self.pk}'

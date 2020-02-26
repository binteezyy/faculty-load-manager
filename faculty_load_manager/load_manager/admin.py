from django.contrib import admin
from django.forms import CheckboxSelectMultiple

from .models import *

# REGISTER ALL
# from django.apps import apps
#
# app = apps.get_app_config('users')
#
# for model_name, model in app.models.items():
#     admin.site.register(model)
#


class PostPreferredTime(admin.ModelAdmin):
    list_display = ('select_day', 'select_time')


class PostPreferredSchedule(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class PostSubject(admin.ModelAdmin):
    list_display = ('subject_name', 'subject_code',
                    'curriculum', 'year_level', 'semester')

class PostBlockSection(admin.ModelAdmin):
    list_display = ('year_level', 'section', 'school_year', 'semester')

class PostSectionOffering(admin.ModelAdmin):
    list_display = ('professor', 'subject', 'block_section')

class PostFacultyLoad(admin.ModelAdmin):
    list_display = ('subject', 'load_category')

class PostRoom(admin.ModelAdmin):
    list_display = ('id', 'room_name','room_category')

admin.site.register(Room, PostRoom)
admin.site.register(Year)
admin.site.register(Subject, PostSubject)
admin.site.register(SchoolYear)
admin.site.register(SemesterOffering)
admin.site.register(SectionOffering, PostSectionOffering)
admin.site.register(PreferredTime, PostPreferredTime)
admin.site.register(PreferredSchedule, PostPreferredSchedule)
admin.site.register(BlockSection, PostBlockSection)
admin.site.register(Curriculum)
admin.site.register(FacultyLoad, PostFacultyLoad)
admin.site.register(LoadSchedule)
# Register your models here.

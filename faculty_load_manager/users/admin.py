from django.contrib import admin

from .models import *

class PostFacultyProfile(admin.ModelAdmin):
    list_display = ('faculty', 'faculty_type', 'regular_hours', 'part_time_hours')

admin.site.register(Setting)
admin.site.register(FacultyProfile, PostFacultyProfile)

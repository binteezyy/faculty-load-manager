from django.contrib import admin

from .models import *

class PostFacultyProfile(admin.ModelAdmin):
    list_display = ('faculty', 'faculty_type', 'regular_hours', 'part_time_hours')

class PostSettings(admin.ModelAdmin):
    list_display = ('school_year','semester','current')

admin.site.register(Setting,PostSettings)
admin.site.register(FacultyProfile, PostFacultyProfile)

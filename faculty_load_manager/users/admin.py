from django.contrib import admin

from .models import *


class PostFacultyProfile(admin.ModelAdmin):
    list_display = ('faculty', 'faculty_type',
                    'regular_hours', 'part_time_hours')


class PostSettings(admin.ModelAdmin):
    list_display = ('school_year', 'semester', 'current')


class PostYSPrefer(admin.ModelAdmin):
    list_display = ('block_section',)


admin.site.register(UserProfile)
admin.site.register(Announcement)
admin.site.register(Setting, PostSettings)
admin.site.register(FacultyProfile, PostFacultyProfile)
admin.site.register(Ys_PreferredSchedule, PostYSPrefer)

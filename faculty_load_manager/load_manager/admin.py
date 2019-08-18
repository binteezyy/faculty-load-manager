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

class PostTimeSelect(admin.ModelAdmin):
    list_display = ('select_day','select_time')


class PostPreferredTime(admin.ModelAdmin):
    list_display = ('user','created_at','updated_at')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

admin.site.register(TimeSelect,PostTimeSelect)
admin.site.register(PreferredSchedule,PostPreferredTime)


# Register your models here.

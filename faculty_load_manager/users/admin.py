from django.contrib import admin
from users.models import *
from django.forms import CheckboxSelectMultiple


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
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
admin.site.register(TimeSelect,PostTimeSelect)
admin.site.register(PreferredTime,PostPreferredTime)

from bootstrap_modal_forms.forms import BSModalForm
from django.shortcuts import render, redirect
from users.models import *

class AnnouncementForm(BSModalForm):
    class Meta:
        model = Announcement
        fields = ['title','message']

class SettingsForm(BSModalForm):
    class Meta:
        model = Setting
        exclude = ['status']


class SectionOfferingProfessorForm(BSModalForm):
    class Meta:
        model = SectionOffering
        fields = ['professor']

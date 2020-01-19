from bootstrap_modal_forms.forms import BSModalForm
from django.shortcuts import render, redirect
from users.models import *


class AnnouncementForm(BSModalForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message']


class SettingsForm(BSModalForm):
    class Meta:
        model = Setting
        exclude = ['status']


class RoomForm(BSModalForm):
    class Meta:
        model = Room
        exclude = ['']


class BlockSectionForm(BSModalForm):
    class Meta:
        model = BlockSection
        exclude = ['']


class UserForm(BSModalForm):
    class Meta:
        model = FacultyProfile
        exclude = ['faculty']


class CurriculumForm(BSModalForm):
    class Meta:
        model = Curriculum
        exclude = ['']


class SectionOfferingProfessorForm(BSModalForm):
    class Meta:
        model = SectionOffering
        fields = ['professor']


class SubjectForm(BSModalForm):
    class Meta:
        model = Subject
        exclude = ['']

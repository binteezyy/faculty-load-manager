from django.urls import reverse_lazy,reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from .model_forms import *
from .models import *
from users.models import *

from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)
login_url = 'home'
import os
from pprint import pprint
# Settings
class SettingsCreateView(LoginRequiredMixin, UserPassesTestMixin,BSModalCreateView):
    template_name = 'load_manager/components/modals/create.html'
    form_class = SettingsForm
    model = Setting
    model_type = 'settings'
    success_message = 'Success: Settings was created.'
    success_url = reverse_lazy('settings')

    def test_func(self):
        return self.request.user.is_superuser
class SettingsReadView(LoginRequiredMixin, UserPassesTestMixin,BSModalReadView):
    model = Setting
    context_object_name = 'setting'
    template_name = 'load_manager/components/modals/read.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewtype'] = 'settings'

        context['first_curriculum'] = kwargs['object'].first_curriculum
        context['first_section'] = kwargs['object'].first_sections
        context['second_curriculum'] = kwargs['object'].second_curriculum
        context['second_section'] = kwargs['object'].second_sections
        context['third_curriculum'] = kwargs['object'].third_curriculum
        context['third_section'] = kwargs['object'].third_sections
        context['fourth_curriculum'] = kwargs['object'].fourth_curriculum
        context['fourth_section'] = kwargs['object'].fourth_sections
        context['fifth_curriculum'] = kwargs['object'].fifth_curriculum
        context['fifth_section'] = kwargs['object'].fifth_sections
        return context
    def test_func(self):
        return self.request.user.is_superuser
class SettingsUpdateView(BSModalUpdateView):
    model = Setting
    template_name = 'load_manager/components/modals/update.html'
    form_class = SettingsForm
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('settings')
class SettingsDeleteView(LoginRequiredMixin, UserPassesTestMixin,BSModalDeleteView):
    model = Setting
    template_name = 'load_manager/components/modals/delete.html'
    context_object_name = 'setting'
    success_message = 'Success: Settings was deleted.'
    success_url = reverse_lazy('settings')
    def test_func(self):
        return self.request.user.is_superuser

# SettingsFacultyPrefer
class SettingsFacultyPreferReadView(LoginRequiredMixin, UserPassesTestMixin,BSModalReadView):
    model = PreferredSchedule
    context_object_name = 'faculty-prefer'
    template_name = 'load_manager/components/modals/read.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewtype'] = 'faculty-prefer'
        context['faculty'] = f"{kwargs['object'].user.first_name} {kwargs['object'].user.last_name}"
        context['psubjs'] = kwargs['object'].preferred_subject.all()
        context['ptime'] = kwargs['object'].preferred_time.all().values_list('select_day','select_time')
        context['times'] = PreferredTime.TIME_SELECT
        context['days'] = DAY_OF_THE_WEEK
        os.system('cls')
        pprint(context['ptime'])
        return context
    def test_func(self):
        return self.request.user.is_superuser
class SettingsFacultyPreferDeleteView(LoginRequiredMixin, UserPassesTestMixin,BSModalDeleteView):
    model = PreferredSchedule
    template_name = 'load_manager/components/modals/delete.html'
    context_object_name = 'faculty_prefer'
    success_message = 'Success: Faculty Preference was deleted.'
    success_url = reverse_lazy('settings')
    def test_func(self):
        return self.request.user.is_superuser

class SectionOfferingCreateView(LoginRequiredMixin, UserPassesTestMixin,BSModalCreateView):
    template_name = 'load_manager/components/modals/create.html'
    form_class = SettingsForm
    model = Setting
    model_type = 'settings'
    success_message = 'Success: Settings was created.'
    success_url = reverse_lazy('settings')

    def test_func(self):
        return self.request.user.is_superuser
class SectionOfferingReadView(LoginRequiredMixin, UserPassesTestMixin,BSModalReadView):
    model = SectionOffering
    context_object_name = 'section-offering'
    template_name = 'load_manager/components/modals/read.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewtype'] = 'section-offering'
        context['section_offering'] = kwargs['object']
        context['professor'] = kwargs['object'].professor
        context['school_year'] = kwargs['object'].school_year
        context['semester'] = kwargs['object'].semester
        context['subject'] = kwargs['object'].subject
        context['block_section'] = kwargs['object'].block_section
        context['service_flag'] = kwargs['object'].service_flag
        return context
    def test_func(self):
        return self.request.user.is_superuser
class SectionOfferingUpdateView(BSModalUpdateView):
    model = SectionOffering
    template_name = 'load_manager/components/modals/update.html'
    form_class = SectionOfferingProfessorForm
    success_message = 'Success: Professor was updated.'
    success_url = reverse_lazy('section-offering')
class SectionOfferingDeleteView(LoginRequiredMixin, UserPassesTestMixin,BSModalDeleteView):
    model = SectionOffering
    template_name = 'load_manager/components/modals/delete.html'
    context_object_name = 'section-offering'
    success_message = 'Success: Settings was deleted.'
    success_url = reverse_lazy('section-offering')
    def test_func(self):
        return self.request.user.is_superuser

class FacultyLoadCreateView(LoginRequiredMixin, UserPassesTestMixin,BSModalCreateView):
    template_name = 'load_manager/components/modals/create.html'
    form_class = SettingsForm
    model = Setting
    model_type = 'settings'
    success_message = 'Success: Settings was created.'
    success_url = reverse_lazy('settings')

    def test_func(self):
        return self.request.user.is_superuser
class FacultyLoadReadView(LoginRequiredMixin, UserPassesTestMixin,BSModalReadView):
    model = FacultyLoad
    context_object_name = 'faculty-load'
    template_name = 'load_manager/components/modals/read.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewtype'] = 'faculty-load'
        context['faculty_load'] = kwargs['object']
        context['preferred_time'] = kwargs['object'].preferred_time
        context['room'] = kwargs['object'].room
        context['subject'] = kwargs['object'].subject
        return context
    def test_func(self):
        return self.request.user.is_superuser
class FacultyLoadUpdateView(BSModalUpdateView):
    model = SectionOffering
    template_name = 'load_manager/components/modals/update.html'
    form_class = SectionOfferingProfessorForm
    success_message = 'Success: Professor was updated.'
    success_url = reverse_lazy('section-offering')
class FacultyLoadDeleteView(LoginRequiredMixin, UserPassesTestMixin,BSModalDeleteView):
    model = SectionOffering
    template_name = 'load_manager/components/modals/delete.html'
    context_object_name = 'section-offering'
    success_message = 'Success: Settings was deleted.'
    success_url = reverse_lazy('section-offering')
    def test_func(self):
        return self.request.user.is_superuser

class SubjectCreateView(LoginRequiredMixin, UserPassesTestMixin,BSModalCreateView):
    template_name = 'load_manager/components/modals/create.html'
    form_class = SettingsForm
    model = Setting
    model_type = 'settings'
    success_message = 'Success: Settings was created.'
    success_url = reverse_lazy('settings')

    def test_func(self):
        return self.request.user.is_superuser
class SubjectReadView(LoginRequiredMixin, UserPassesTestMixin,BSModalReadView):
    model = Subject
    context_object_name = 'semester-offering-subject'
    template_name = 'load_manager/components/modals/read.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewtype'] = 'subject'
        context['subject'] = kwargs['object']
        context['year_level'] = kwargs['object'].year_level
        context['subject_code'] = kwargs['object'].subject_code
        context['subject_name'] = kwargs['object'].subject_name
        context['curriculum'] = kwargs['object'].curriculum
        context['offered'] = kwargs['object'].offered
        context['lab_hours'] = kwargs['object'].lab_hours
        context['lec_hours'] = kwargs['object'].lec_hours
        context['room_category'] = kwargs['object'].get_room_category_display
        return context
    def test_func(self):
        return self.request.user.is_superuser
class SubjectUpdateView(BSModalUpdateView):
    model = SectionOffering
    template_name = 'load_manager/components/modals/update.html'
    form_class = SectionOfferingProfessorForm
    success_message = 'Success: Professor was updated.'
    success_url = reverse_lazy('section-offering')
class SubjectDeleteView(LoginRequiredMixin, UserPassesTestMixin,BSModalDeleteView):
    model = SectionOffering
    template_name = 'load_manager/components/modals/delete.html'
    context_object_name = 'section-offering'
    success_message = 'Success: Settings was deleted.'
    success_url = reverse_lazy('section-offering')
    def test_func(self):
        return self.request.user.is_superuser

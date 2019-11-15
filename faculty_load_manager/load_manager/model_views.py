from django.urls import reverse_lazy,reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required,user_passes_test
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

class AnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin,BSModalCreateView):
    template_name = 'load_manager/components/modals/create.html'
    form_class = AnnouncementForm
    model = Announcement
    model_type = 'annoucement'
    success_message = 'Success: Settings was created.'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.category = 0
        return super().form_valid(form)
class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin,BSModalDeleteView):
    model = Announcement
    template_name = 'load_manager/components/modals/delete.html'
    context_object_name = 'annoucement'
    success_message = 'Success: Annoucement was deleted.'
    success_url = reverse_lazy('home')
    def test_func(self):
        return self.request.user.is_superuser
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

#Room
class RoomCreateView(LoginRequiredMixin, UserPassesTestMixin,BSModalCreateView):
    template_name = 'load_manager/components/modals/create.html'
    form_class = RoomForm
    model = Room
    model_type = 'room'
    success_message = 'Success: Room was created.'
    success_url = reverse_lazy('room')

    def test_func(self):
        return self.request.user.is_superuser
class RoomDeleteView(LoginRequiredMixin, UserPassesTestMixin,BSModalDeleteView):
    model = Room
    template_name = 'load_manager/components/modals/delete.html'
    context_object_name = 'room'
    success_message = 'Success: Room was deleted.'
    success_url = reverse_lazy('room')
    def test_func(self):
        return self.request.user.is_superuser

class RoomUpdateView(BSModalUpdateView):
    model = Room
    template_name = 'load_manager/components/modals/update.html'
    form_class = RoomForm
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('room')

#SECTIONS
class SectionCreateView(LoginRequiredMixin, UserPassesTestMixin,BSModalCreateView):
    template_name = 'load_manager/components/modals/create.html'
    form_class = BlockSectionForm
    model = BlockSection
    model_type = 'block-sections'
    success_message = 'Success: Section was created.'
    success_url = reverse_lazy('sections')

    def test_func(self):
        return self.request.user.is_superuser
class SectionsDeleteView(LoginRequiredMixin, UserPassesTestMixin,BSModalDeleteView):
    model = BlockSection
    template_name = 'load_manager/components/modals/delete.html'
    context_object_name = 'block_section'
    success_message = 'Success: Section was deleted.'
    success_url = reverse_lazy('sections')
    def test_func(self):
        return self.request.user.is_superuser

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def SectionsUpdateView(request,pk):
    settings = Setting.objects.get(current=True)
    time_schedules = PreferredTime.objects.all()
    current_user = request.user
    subjs = SemesterOffering.objects.get(school_year=settings.school_year,semester=settings.semester).subject.all()

    context = {
        'title': 'LOAD MANAGER | FORM',
        'viewtype': 'load-manager',
        'user': request.user,
        'subjects': subjs,
        'time_schedules': time_schedules,
        'days': DAY_OF_THE_WEEK,
        'times': PreferredTime.TIME_SELECT,
    }
    if request.method=="POST":
        os.system('cls')
        selected = request.POST.getlist('timedays')
        subjects = request.POST.getlist('psubjects')
        print(subjects)
        setting = Setting.objects.get(current=True)
        current_user = request.user
        preferred_sched =  PreferredSchedule(user = current_user,
                                            semester = setting.semester,
                                            school_year = setting.school_year)

        preferred_sched.save()
        for x in selected:
            daytime = x.split('-')
            print(daytime)
            d = PreferredTime.objects.filter(select_time=daytime[1]).get(select_day=daytime[0])
            preferred_sched.preferred_time.add(d)
        for x in subjects:
            d = Subject.objects.get(pk=x)
            preferred_sched.preferred_subject.add(d)
        return redirect('load-manager-list')
    else:
        return render(request, 'load_manager/components/chairperson/sections/modals/update.html', context)
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

class CurriculumUpdateView(BSModalUpdateView):
    model = Curriculum
    template_name = 'load_manager/components/modals/update.html'
    form_class = CurriculumForm
    success_message = 'Success: Curriculum was updated.'
    success_url = reverse_lazy('settings-curriculum')

class CurriculumDeleteView(LoginRequiredMixin, UserPassesTestMixin,BSModalDeleteView):
    model = Curriculum
    template_name = 'load_manager/components/modals/delete.html'
    context_object_name = 'curriculum'
    success_message = 'Success: Settings was deleted.'
    success_url = reverse_lazy('ssettings-curriculum')
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

class RoomReadView(LoginRequiredMixin, UserPassesTestMixin,BSModalReadView):
    model = Room
    context_object_name = 'semester-offering-subject'
    template_name = 'load_manager/components/modals/read.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewtype'] = 'room'
        context['subject'] = kwargs['object']
        context['times'] = PreferredTime.TIME_SELECT
        context['days'] = DAY_OF_THE_WEEK
        context["room_sched"] = FacultyLoad.objects.filter(load_schedule__room = kwargs['object'])
        return context
    def test_func(self):
        return self.request.user.is_superuser

# Settings
class UserCreateView(LoginRequiredMixin, UserPassesTestMixin,BSModalCreateView):
    template_name = 'load_manager/components/modals/create.html'
    form_class = SettingsForm
    model = Setting
    model_type = 'settings'
    success_message = 'Success: Settings was created.'
    success_url = reverse_lazy('settings')

    def test_func(self):
        return self.request.user.is_superuser
class UserReadView(LoginRequiredMixin, UserPassesTestMixin,BSModalReadView):
    model = User
    context_object_name = 'user'
    template_name = 'load_manager/components/modals/read.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewtype'] = 'user'
        context['first_name'] = kwargs['object'].first_name
        context['last_name'] = kwargs['object'].last_name
        context['img'] = UserProfile.objects.get(user=kwargs['object']).avatar
        return context
    def test_func(self):
        return self.request.user.is_superuser
class UserUpdateView(BSModalUpdateView):
    model = FacultyProfile
    template_name = 'load_manager/components/modals/update.html'
    form_class = UserForm
    success_message = 'Success: Profile was updated.'
    success_url = reverse_lazy('chairperson-upm')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewtype'] = 'user'
        return context
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin,BSModalDeleteView):
    model = User
    template_name = 'load_manager/components/modals/delete.html'
    context_object_name = 'faculty'
    success_message = 'Success: User was deleted.'
    success_url = reverse_lazy('chairperson-upm')
    def test_func(self):
        return self.request.user.is_superuser

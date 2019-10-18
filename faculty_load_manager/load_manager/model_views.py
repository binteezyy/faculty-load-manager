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

    # def dispatch(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     success_url = reverse_lazy('settings')
    #     settings = Setting.objects.get(id=kwargs['pk'])
    #     if settings.current == True:
    #         pass
    #     else:
    #         return super(SettingsDeleteView, self).delete(request, *args, **kwargs)

from django.urls import reverse_lazy
from django.views import generic
from .forms import *
from .models import *
from users.models import *

from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)

# Settings
class SettingsCreateView(BSModalCreateView):
    template_name = 'load_manager/components/modals/create.html'
    form_class = SettingsForm
    model_type = 'settings'
    success_message = 'Success: Settings was created.'
    success_url = reverse_lazy('settings')

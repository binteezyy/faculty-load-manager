from bootstrap_modal_forms.forms import BSModalForm
from users.models import *

class SettingsForm(BSModalForm):
    class Meta:
        model = Setting
        exclude = ['status']

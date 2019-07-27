from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserLoginForm(forms.Form):
    username = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('User does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('User is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.EmailField(label='Email address')
    username2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'username2',
            'password',
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        username2 = self.cleaned_data.get('username2')
        # username = self.cleaned_data.get('username')

        if username != username2:
            raise forms.ValidationError("Emails does not match")
        
        email_q = User.objects.filter(username=username)
        # username_q = User.objects.filter(username=username)
        # if username_q.exists():
        #     raise forms.ValidationError("Username already registered")
        if email_q.exists():
            raise forms.ValidationError("Email already registered")

        return super(UserRegisterForm, self).clean(*args, **kwargs)
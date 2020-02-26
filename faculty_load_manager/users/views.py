from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import (
    authenticate,
    logout,
    login,
    views as auth_views
)
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from .models import *
import os
import random
import string

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'password/password_reset_form.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password-reset-done')
    subject_template_name = 'password/password_reset_subject.txt'
    email_template_name = 'password/password_reset_email.html'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password/password_reset_confirm.html'
    success_url = reverse_lazy('home')
    form_valid_message = ("Your password was changed!")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
def randomPassword():
    """Generate a random password """
    randomSource = string.ascii_letters + string.digits + string.punctuation
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += random.choice(string.punctuation)

    for i in range(6):
        password += random.choice(randomSource)

    passwordList = list(password)
    random.SystemRandom().shuffle(passwordList)
    password = ''.join(passwordList)
    return password

@login_required
def user_profile(request,pk):
    if request.method == 'POST':
        return redirect('user-profile',pk = request.user.pk )
    else:
        context = {
                'user': request.user,
                'avatar': UserProfile.objects.get(user=request.user).avatar,
                'user_type': FacultyProfile.objects.get(faculty=request.user).get_faculty_type_display,
                'viewtype': 'user-profile',
                'title': 'USER POOL',
        }
        return render(request, 'load_manager/components/chairperson/users-management/profile.html', context)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_pool_management(request):
    context = {
            'viewtype': 'user-pool-management',
            'title': 'USER POOL',
            'avatar': UserProfile.objects.get(user=request.user).avatar,
    }
    return render(request, 'load_manager/components/chairperson/users-management/index.html', context)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_pool_mangement_table(request):
    import json
    from pprint import pprint
    users = User.objects.all()

    data = []
    for user in users:
        profile = FacultyProfile.objects.get(faculty=user.id)
        x = {"fields":{"id":[user.pk,profile.pk],
                       "user-fname":user.first_name,
                       "user-lname":user.last_name,
                       "user-email":user.email,
                       "user-type": profile.get_faculty_type_display(),
                       "user-rhours":profile.regular_hours,
                       "user-pthours":profile.part_time_hours,
             }
        }
        data.append(x)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_pool_management_create(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        ftype = request.POST.get('type')


        try:
            user = User.objects.create_user(username=username,
                                             email=email,
                                             password="",
                                             first_name=fname,
                                             last_name=lname
                                             )
            profile = FacultyProfile.objects.get(faculty=user)
            profile.faculty_type = int(ftype)
            if ftype == '0': #Part-Time
                profile.regular_hours = 0
                profile.part_time_hours = 12
            elif ftype == '1': #Regular
                profile.regular_hours = 15
                profile.part_time_hours = 12
            elif ftype == '2': #Chief
                profile.regular_hours = 6
                profile.part_time_hours = 12
            elif ftype == '3': #Director
                profile.regular_hours = 3
                profile.part_time_hours = 12
            else:
                profile.delete()
                raise ValueError('Invalid Faculty Type')


            profile.save()


        except Exception as e:
            user.delete()
            raise e
        return redirect('chairperson-upm')
    else:
        x = FacultyProfile.F_TYPE
        print(x)
        context = {
            'faculty_type': x,
        }
        return render(request, 'load_manager/components/chairperson/users-management/add-users.html', context)

@login_required
def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.is_staff=False
        user.save()

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)

        if next:
            return redirect(next)
        return HttpResponseRedirect(reverse('home'))

    context = {
        'form':form,
        'title':'Register',
    }
    return render(request, 'users/components/register.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

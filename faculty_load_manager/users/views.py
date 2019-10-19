from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import (
    authenticate,
    logout,
    login
)
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm
from django.contrib.auth.models import User

from .models import *
import os
import random
import string
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
@user_passes_test(lambda u: u.is_superuser)
def user_pool_management(request):
    context = {
            'viewtype': 'user-pool-management',
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
        x = {"fields":{"user-fname":user.first_name,
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
        type = request.POST.get('type')

        r = randomPassword()
        user = User.objects.create_user(username=username,
                                         email=email,
                                         password=r,
                                         first_name=fname,
                                         last_name=lname
                                         )
        profile = FacultyProfile.objects.get(faculty=user)
        try:
            if type == '0':
                profile.regular_hours = 0
                profile.part_time_hours = 12
            elif type == '1':
                profile.regular_hours = 15
                profile.part_time_hours = 12
            elif type == '2':
                profile.regular_hours = 6
                profile.part_time_hours = 12
            elif type == '3':
                profile.regular_hours = 3
                profile.part_time_hours = 12
            else:
                user.delete()
                raise ValueError('Invalid Faculty Type')

            profile.save()
            subject = 'Welcome to Computer Engineering Faculty Website'
            message = f'Hi {fname}! You have been registered. Here is your temporary password:  {r}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail( subject, message, email_from, recipient_list )
        except Exception as e:
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

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import (
    authenticate,
    logout,
    login
)

from .forms import UserRegisterForm
from django.contrib.auth.models import User

from .models import *

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_pool_management(request):
    context = {
            'viewtype': 'user-pool-management',
    }
    return render(request, 'load_manager/components/chairperson/user-pool-management.html', context)
@login_required
def user_pool_mangement_table(request):
    import json
    from pprint import pprint
    users = User.objects.all()

    data = []
    for user in users:
        profile = FacultyProfile.objects.get(id=user.id)
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
    pprint(data)
    return HttpResponse(data, content_type='application/json')

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

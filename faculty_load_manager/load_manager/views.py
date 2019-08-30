from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required,user_passes_test
from .models import *
# Create your views here.
from pprint import pprint
from django.contrib.auth import (
    authenticate,
    login,
)

from django.contrib.auth.decorators import login_required
from users.models import *

from django.contrib.auth import login
from .forms import UserLoginForm, UserRegisterForm

def home_view(request):
    next = request.GET.get('next')

    if request.user.is_authenticated:
        context = {
            'user': request.user,
        }
        return render(request, 'load_manager/components/home.html', context)
    else:
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            login(request, user)

            if next:
                return redirect(next)
            return HttpResponseRedirect(reverse('home'))

        context = {
            'form': form,
            'title': 'Login',
        }
        return render(request, 'users/components/login.html', context)

@login_required
def pload_view(request):
    time_schedules = PreferredTime.objects.all()
    current_user = request.user
    context = {
        'user': request.user,
        'time_schedules': time_schedules,
        'days': DAY_OF_THE_WEEK,
        'times': PreferredTime.TIME_SELECT,
    }
    if request.method=="POST":
        selected = request.POST.getlist('timedays')
        current_user = request.user
        preferred_sched =  PreferredSchedule(user = current_user)

        preferred_sched.save()
        for x in selected:
            daytime = x.split('-')
            print(daytime)
            d = PreferredTime.objects.filter(select_time=daytime[1]).get(select_day=daytime[0])
            preferred_sched.preferred_time.add(d)

        return HttpResponse("POSTED")
    else:
        return render(request, 'load_manager/components/pload.html', context)
@login_required
def ss(request):
    for x,day in DAY_OF_THE_WEEK():
        for y, day in PreferredTime.TIME_SELECT:
            sched = PreferredTime.objects.create(
                select_day = x,
                select_time = y
            )
            sched.save()

    return HttpResponse("SCHEDS CREATED")
@login_required
@user_passes_test(lambda u: u.is_superuser)
def site_settings(request):
    context = {
        'school_year': SchoolYear.objects.all(),
        'semester': SEMESTERS(),
    }
    settings = Setting.objects.get_or_create()

    return render(request, 'load_manager/components/settings.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def change_settings(request):
    if request.is_ajax():
        attr = request.POST.get('data-attr')
        data = request.POST.get('data')
        print(attr + '\t' + data)
        settings = Setting.objects.get(id=1)
        if attr == 'SchoolYear':
            settings.school_year = SchoolYear.objects.get(pk=data)
        elif attr == 'Semester':
            settings.semester = data
        settings.save()
    else:
        print("NO AJAX")

    return HttpResponse("POSTED")

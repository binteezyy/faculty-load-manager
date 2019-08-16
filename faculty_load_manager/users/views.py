from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from .forms import UserLoginForm, UserRegisterForm

from django.contrib.auth.decorators import login_required
from users.models import *
# Create your views here.
from pprint import pprint
@login_required(login_url='/login/')
def home_view(request):

    context = {
        'user': request.user,
    }
    return render(request, 'components/home.html', context)

def login_view(request):
    next = request.GET.get('next')

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
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
        return render(request, 'components/login.html', context)

def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
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
    return render(request, 'components/register.html', context)

def pload_view(request):
    time_schedules = TimeSelect.objects.all()
    current_user = request.user
    context = {
        'user': request.user,
        'time_schedules': time_schedules,
        'days': TimeSelect.DAY_OF_THE_WEEK,
        'times': TimeSelect.TIME_SELECT,
    }
    if request.method=="POST":
        selected = request.POST.getlist('timedays')
        current_user = request.user
        preferred_sched =  PreferredSchedule(user = current_user)

        preferred_sched.save()
        pprint(selected)
        for x in selected:
            daytime = x.split('-')
            print(daytime)
            d = TimeSelect.objects.filter(select_time=daytime[1]).get(select_day=daytime[0])
            preferred_sched.preferred_time.add(d)

        return HttpResponse("POSTED")
    else:
        return render(request, 'components/pload.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required
def ss(request):
    for x,day in TimeSelect.DAY_OF_THE_WEEK:
        for y, day in TimeSelect.TIME_SELECT:
            sched = TimeSelect.objects.create(
                select_day = x,
                select_time = y
            )
            sched.save()

    return HttpResponse("SCHEDS CREATED")

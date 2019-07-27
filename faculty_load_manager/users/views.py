from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from .forms import UserLoginForm, UserRegisterForm

from django.contrib.auth.decorators import login_required
# Create your views here.

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
        password = form.cleaned_data('password')
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)

        if next:
            return redirect(next)
        return HttpResponseRedirect(reverse('home'))

    context = {
        'form':form,
    }
    return render(request, 'components/register.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

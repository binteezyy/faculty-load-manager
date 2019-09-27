from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import (
    authenticate,
    logout,
    login
)

from .forms import UserRegisterForm

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_pool_management(request):
    context = {
            'viewtype': 'user-pool-management',
    }
    return render(request, 'load_manager/components/chairperson/user-pool-management.html', context)
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

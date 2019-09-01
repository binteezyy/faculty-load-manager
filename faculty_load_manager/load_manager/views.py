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
    curriculum = Curriculum.objects.all()
    context = {
        'school_year': SchoolYear.objects.all(),
        'semester': SEMESTERS(),
        'curriculum': curriculum,
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
        elif attr == 'Curriculum':
            settings.curriculum = Curriculum.objects.get(pk=data)
        settings.save()
    else:
        print("NO AJAX")

    return HttpResponse("POSTED")

from bs4 import BeautifulSoup
import re
from pprint import pprint

def parse_view(request):
    semester = 0
    year_level = 1
    url = '/home/binpngnbn/Downloads/1112.html'
    curriculum = ((url.split('/')[-1]).split('.')[0])
    page = open(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    tables = soup.findAll('table') #get tables

    try:
        curriculum_get = Curriculum.objects.get(curriculum=str(curriculum))
    except Curriculum.DoesNotExist:
        new_curriculum = Curriculum(curriculum=str(curriculum))
        new_curriculum.save()
    
    curriculum_get = Curriculum.objects.get(curriculum=str(curriculum))

    for x in range(2,int(len(tables))): #run through tables from tables[2]
        table = tables[x]
        trs = table.findAll('tr')       #get table rows

        for y in range(1, int(len(trs))): #run through table rows from rows[1]
            try:
                code = trs[y].findAll('td')[0].contents #get course code
                strcode = ''.join(code)
            except:
                code = 'None'
            try:
                description = trs[y].findAll('td')[3].contents #get course description
                strdesc = ''.join(description)
            except:
                description = 'None'
            try:
                lec_hours = trs[y].findAll('td')[4].contents #get lecture hours
                strlec = ''.join(lec_hours)
            except:
                lec_hours = 'None'
            try:
                lab_hours = trs[y].findAll('td')[5].contents #get lab hours
                strlab = ''.join(lab_hours)
            except:
                lab_hours = 'None'
            
            if strcode == 'TOTAL UNITS':
                if semester == 2:
                    semester = 0
                    year_level += 1
                else:
                    semester += 1
            else:
                try:
                    get_subj = Subject.objects.get(subject_code=strcode, subject_name=strdesc)
                except Subject.DoesNotExist:
                    new_subj = Subject(year_level=year_level, semester=semester, curriculum=curriculum_get,
                    subject_code=strcode, subject_name=strdesc, lab_hours=int(strlab), lec_hours=int(strlec))
                    new_subj.save()

                print(f'{strcode} - {strdesc} - {strlab} - {strlec}')


    return HttpResponse("PARSED")

from django.db.models import Q

def generate_semester_offering(request):
    first_c = Curriculum.objects.get(curriculum='1112')
    second_c = Curriculum.objects.get(curriculum='1112')
    third_c = Curriculum.objects.get(curriculum='1112')
    fourth_c = Curriculum.objects.get(curriculum='1112')
    fifth_c = Curriculum.objects.get(curriculum='1112')
    semester = 0
    start_year = 2020
    end_year = 2021

    try:
        start = Year.objects.get(year=start_year)
    except Year.DoesNotExist:
        new_year = Year(year=start_year)
        new_year.save()
        start = Year.objects.get(year=start_year)
    
    try:
        end = Year.objects.get(year=end_year)
    except Year.DoesNotExist:
        new_year = Year(year=end_year)
        new_year.save()
        end  = Year.objects.get(year=end_year)

    try:
        sy = SchoolYear.objects.get(start_year=start, end_year=end)
    except SchoolYear.DoesNotExist:
        new_sy = SchoolYear(start_year=start, end_year=end)
        new_sy.save()
        sy = SchoolYear.objects.get(start_year=start, end_year=end)
    
    try:
        semOff = SemesterOffering.objects.get(school_year=sy, semester=semester)
    except SemesterOffering.DoesNotExist:
        # return HttpResponse("Does Not")
        new_so = SemesterOffering.objects.create(school_year=sy, semester=semester)
        new_so.save()

        semOff = SemesterOffering.objects.get(school_year=sy, semester=semester)
    
        first_s = Subject.objects.filter(year_level=1, semester=semester, curriculum=first_c).filter(
            Q(subject_code__startswith='COEN')|Q(subject_code__startswith='BSCOE'))
        second_s = Subject.objects.filter(year_level=2, semester=semester, curriculum=second_c).filter(
            Q(subject_code__startswith='COEN')|Q(subject_code__startswith='BSCOE'))
        third_s = Subject.objects.filter(year_level=3, semester=semester, curriculum=third_c).filter(
            Q(subject_code__startswith='COEN')|Q(subject_code__startswith='BSCOE'))
        fourth_s = Subject.objects.filter(year_level=4, semester=semester, curriculum=fourth_c).filter(
            Q(subject_code__startswith='COEN')|Q(subject_code__startswith='BSCOE'))
        fifth_s = Subject.objects.filter(year_level=5, semester=semester, curriculum=fifth_c).filter(
            Q(subject_code__startswith='COEN')|Q(subject_code__startswith='BSCOE'))

        first_s = list(first_s)
        second_s = list(second_s)
        third_s = list(third_s)
        fourth_s = list(fourth_s)
        fifth_s = list(fifth_s)
        print(first_s)
        semOff.subject.add(*first_s)
        print(second_s)
        semOff.subject.add(*second_s)
        print(third_s)
        semOff.subject.add(*third_s)
        print(fourth_s)
        semOff.subject.add(*fourth_s)
        print(fifth_s)
        semOff.subject.add(*fifth_s)
        semOff.save()

    context = {
        'subjects': semOff.subject.all(),
    }

    return HttpResponse(semOff.subject.all())



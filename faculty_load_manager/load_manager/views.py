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
            'viewtype': 'home',
            'title': 'Home'
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
def load_manager_list(request):
    settings = Setting.objects.get(pk=1)
    if PreferredSchedule.objects.filter(user=request.user,school_year=settings.school_year,semester=settings.semester).exists():
        cs = True
        psched = PreferredSchedule.objects.get(user=request.user,school_year=settings.school_year,semester=settings.semester)
    else:
        cs = False
        psched = ""
    context = {
        'title': 'LOAD MANAGER',
        'viewtype': 'load-manager',
        'submission': cs,
        'psubj': psched,
    }
    return render(request, 'load_manager/components/faculty-load/list.html', context)

#===================================================
#                   LOAD MANAGER
#===================================================
@login_required
def load_manager_tables(request):
    import json
    loads = PreferredSchedule.objects.filter(user=request.user)

    data = []
    for load in loads:
        print(load.semester)
        x = {"fields":{"id":load.pk,
                       "date_submit":load.created_at.strftime("%d-%m-%Y %I:%M%p"),
                       "school_year": str(load.school_year),
                       "semester": str(load.get_semester_display()),
                       "details": "",
                       "status": "",
             }
        }
        data.append(x)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
@login_required
def load_manager_create(request):
    settings = Setting.objects.get(pk=1)
    time_schedules = PreferredTime.objects.all()
    current_user = request.user
    subjs = SemesterOffering.objects.get(school_year=settings.school_year,semester=settings.semester).subject.all()

    context = {
        'title': 'LOAD MANAGER | FORM',
        'viewtype': 'load-manager',
        'user': request.user,
        'subjects': subjs,
        'time_schedules': time_schedules,
        'days': DAY_OF_THE_WEEK,
        'times': PreferredTime.TIME_SELECT,
    }
    if request.method=="POST":
        selected = request.POST.getlist('timedays')
        subjects = request.POST.getlist('psubjects')
        print(subjects)
        setting = Setting.objects.get(pk=1)
        current_user = request.user
        preferred_sched =  PreferredSchedule(user = current_user,
                                            semester = setting.semester,
                                            school_year = setting.school_year)

        preferred_sched.save()
        for x in selected:
            daytime = x.split('-')
            print(daytime)
            d = PreferredTime.objects.filter(select_time=daytime[1]).get(select_day=daytime[0])
            preferred_sched.preferred_time.add(d)
        for x in subjects:
            d = Subject.objects.get(pk=x)
            preferred_sched.preferred_subject.add(d)
        return redirect('load-manager-list')
    else:
        return render(request, 'load_manager/components/pload.html', context)

#===================================================
#                   UTILITIES
#===================================================
@login_required
def ss(request):
    for x,day in DAY_OF_THE_WEEK():
        for y, day in PreferredTime.TIME_SELECT:
            try:
                sched = PreferredTime.objects.get(
                select_day = x,
                select_time = y
                )
                print(f'{x} {y} already exists')
            except PreferredTime.DoesNotExist:
                sched = PreferredTime(
                    select_day = x,
                    select_time = y
                )
                sched.save()
    try:
        x = Room.objects.get(room_name='310', room_category=1)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='310', room_category=1)
        x.save()
    try:
        x = Room.objects.get(room_name='311', room_category=0)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='311', room_category=0)
        x.save()
    try:
        x = Room.objects.get(room_name='312', room_category=0)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='312', room_category=0)
        x.save()
    try:
        x = Room.objects.get(room_name='313', room_category=0)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='313', room_category=0)
        x.save()
    try:
        x = Room.objects.get(room_name='314', room_category=0)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='314', room_category=0)
        x.save()
    try:
        x = Room.objects.get(room_name='315', room_category=0)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='315', room_category=0)
        x.save()
    try:
        x = Room.objects.get(room_name='300', room_category=0)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='300', room_category=0)
        x.save()
    try:
        x = Room.objects.get(room_name='302', room_category=1)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='302', room_category=1)
        x.save()
    try:
        x = Room.objects.get(room_name='316', room_category=1)
        print('Exists')
    except Room.DoesNotExist:
        x = Room(room_name='316', room_category=1)
        x.save()
    return HttpResponse("SCHEDS CREATED")

#===================================================
#               CHAIRPERSON VIEW
#===================================================
@login_required
@user_passes_test(lambda u: u.is_superuser)
def site_settings(request):
    curriculum = Curriculum.objects.all()
    context = {
        'viewtype': 'settings',
        'school_year': SchoolYear.objects.all(),
        'semesters': SEMESTERS(),
        'curriculum': curriculum,
    }
    # settings = Setting.objects.get_or_create()

    return render(request, 'load_manager/components/chairperson/settings/settings.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def site_settings_table(request):
    import json
    from pprint import pprint
    settings = Setting.objects.all()
    data = []
    for setting in settings:
        x = {"fields":{"id":setting.pk,
                       "sy":[setting.pk,str(setting.school_year)],
                       "semester":setting.get_semester_display(),
             }
        }
        data.append(x)
    pprint(data)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')



@login_required
@user_passes_test(lambda u: u.is_superuser)
def curriculum_settings(request):
    curriculums = Curriculum.objects.all()
    context = {
        'viewtype': 'curriculum',
        'curriculums': curriculums,
    }

    return render(request, 'load_manager/components/chairperson/curriculum.html', context)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def curriculum_settings_subject(request,pk):
    import json
    from pprint import pprint
    subjects = Subject.objects.filter(curriculum=pk)
    data = []
    for subject in subjects:
        x = {"fields":{"subject-name":subject.subject_name,
                       "subject-code":subject.subject_code,
                       "year-level":subject.year_level,
                       "semester":subject.get_semester_display()

             }
        }
        data.append(x)
    data = json.dumps(data)
    pprint(data)
    return HttpResponse(data, content_type='application/json')

    return HttpResponse(subjects)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def curriculum_settings_table(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        type = request.POST.get('type')
        import os
        os.system('cls')
        print(fname,lname)
        print(email,type)
        return redirect('chairperson-upm')
    else:
        x = FacultyProfile.F_TYPE
        print(x)
        context = {
            'faculty_type': x,
        }
        return render(request, 'load_manager/components/chairperson/users-management/add-users.html', context)

from bs4 import BeautifulSoup
import re
from pprint import pprint

from django.core.files.storage import FileSystemStorage
@login_required
@user_passes_test(lambda u: u.is_superuser)
def curriculum_upload(request):

    if request.method == 'GET':
        context = {}
        return render(request, 'load_manager/components/chairperson/curriculum-upload.html', context)

    elif request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = (str(settings.BASE_DIR) + str(fs.url(filename))).replace('/', '\\') #if deployed on windows
        # return HttpResponse(uploaded_file_url)
        # PARSE

        semester = 0
        year_level = 1
        url = uploaded_file_url
        curriculum = (((url.split('/')[-1]).split('.')[0]).split('\\')[-1]).split('_')[0]
        # return HttpResponse(curriculum)
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

        return redirect('settings-curriculum')


from bs4 import BeautifulSoup
import re
from pprint import pprint

def parse_view(request):
    semester = 0
    year_level = 1
    url = 'C:/Users/Bin/Downloads/1112.html'
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
    settings = Setting.objects.all()[0]
    first_c = Curriculum.objects.get(curriculum=settings.first_curriculum.curriculum)
    second_c = Curriculum.objects.get(curriculum=settings.second_curriculum.curriculum)
    third_c = Curriculum.objects.get(curriculum=settings.third_curriculum.curriculum)
    fourth_c = Curriculum.objects.get(curriculum=settings.fourth_curriculum.curriculum)
    fifth_c = Curriculum.objects.get(curriculum=settings.fifth_curriculum.curriculum)
    semester = str(settings.semester)
    start_year = str(settings.school_year.start_year)
    end_year = str(settings.school_year.end_year)

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

def generate_section_offering(request):
    settings = Setting.objects.all()[0]
    semester = str(settings.semester)
    start_year = str(settings.school_year.start_year)
    end_year = str(settings.school_year.end_year)

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
        fifth_count = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=5).count()
    except:
        fifth_count = 0
    print(f'fifth year - {fifth_count}')
    try:
        fourth_count = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=4).count()
    except:
        fourth_count = 0
    print(f'fourth year - {fourth_count}')
    try:
        third_count = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=3).count()
    except:
        third_count = 0
    print(f'third year - {third_count}')
    try:
        second_count = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=2).count()
    except:
        second_count = 0
    print(f'second year - {second_count}')
    try:
        first_count = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=1).count()
    except:
        first_count = 0
    print(f'first year - {first_count}')

    semOff = SemesterOffering.objects.get(school_year=sy, semester=semester)
    # first_s = Subject.objects.filter(year_level=1, semester=semester, curriculum=first_c).filter(
    #         Q(subject_code__startswith='COEN')|Q(subject_code__startswith='BSCOE'), thesis_flag=False)
    # second_s = Subject.objects.filter(year_level=2, semester=semester, curriculum=second_c).filter(
    #         Q(subject_code__startswith='COEN')|Q(subject_code__startswith='BSCOE'), thesis_flag=False)
    # third_s = Subject.objects.filter(year_level=3, semester=semester, curriculum=third_c).filter(
    #         Q(subject_code__startswith='COEN')|Q(subject_code__startswith='BSCOE'), thesis_flag=False)
    # fourth_s = Subject.objects.filter(year_level=4, semester=semester, curriculum=fourth_c).filter(
    #         Q(subject_code__startswith='COEN')|Q(subject_code__startswith='BSCOE'), thesis_flag=False)
    # fifth_s = Subject.objects.filter(year_level=5, semester=semester, curriculum=fifth_c).filter(
    #         Q(subject_code__startswith='COEN')|Q(subject_code__startswith='BSCOE'), thesis_flag=False)
    first_s = semOff.subject.all().filter(year_level=1)
    second_s = semOff.subject.all().filter(year_level=2)
    third_s = semOff.subject.all().filter(year_level=3)
    fourth_s = semOff.subject.all().filter(year_level=4)
    fifth_s = semOff.subject.all().filter(year_level=5)

    if fifth_count > 0 and fifth_s.count() > 0:
        for i in range(fifth_count):
            bs = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=5)[i]
            for j in range(fifth_s.count()):
                try:
                    new_secOff = SectionOffering.objects.get(school_year=sy, semester=semester, subject=fifth_s[j],
                    block_section=bs)
                except SectionOffering.DoesNotExist:
                    new_secOff = SectionOffering(school_year=sy, semester=semester, subject=fifth_s[j],
                    block_section=bs)
                    new_secOff.save()
                print(new_secOff)

    if fourth_count > 0 and fourth_s.count() > 0:
        for i in range(fourth_count):
            bs = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=4)[i]
            for j in range(fourth_s.count()):
                try:
                    new_secOff = SectionOffering.objects.get(school_year=sy, semester=semester, subject=fourth_s[j],
                    block_section=bs)
                except SectionOffering.DoesNotExist:
                    new_secOff = SectionOffering(school_year=sy, semester=semester, subject=fourth_s[j],
                    block_section=bs)
                    new_secOff.save()
                print(new_secOff)

    if third_count > 0 and third_s.count() > 0:
        for i in range(third_count):
            bs = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=3)[i]
            for j in range(third_s.count()):
                try:
                    new_secOff = SectionOffering.objects.get(school_year=sy, semester=semester, subject=third_s[j],
                    block_section=bs)
                except SectionOffering.DoesNotExist:
                    new_secOff = SectionOffering(school_year=sy, semester=semester, subject=third_s[j],
                    block_section=bs)
                    new_secOff.save()
                print(new_secOff)

    if second_count > 0 and second_s.count() > 0:
        for i in range(second_count):
            bs = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=2)[i]
            for j in range(second_s.count()):
                try:
                    new_secOff = SectionOffering.objects.get(school_year=sy, semester=semester, subject=second_s[j],
                    block_section=bs)
                except SectionOffering.DoesNotExist:
                    new_secOff = SectionOffering(school_year=sy, semester=semester, subject=second_s[j],
                    block_section=bs)
                    new_secOff.save()
                print(new_secOff)

    if first_count > 0 and first_s.count() > 0:
        for i in range(first_count):
            bs = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=1)[i]
            for j in range(first_s.count()):
                try:
                    new_secOff = SectionOffering.objects.get(school_year=sy, semester=semester, subject=first_s[j],
                    block_section=bs)
                except SectionOffering.DoesNotExist:
                    new_secOff = SectionOffering(school_year=sy, semester=semester, subject=first_s[j],
                    block_section=bs)
                    new_secOff.save()
                print(new_secOff)


    return HttpResponse("generated section offering")

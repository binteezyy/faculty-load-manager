from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
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

import os
import json
import re
from bs4 import BeautifulSoup

def home_view(request):
    next = request.GET.get('next')
    status = ''
    try:
        csettings = Setting.objects.get(current=True)
        status = csettings.get_status_display
        announcements = Announcements.objects.order_by('-created')[:5]
    except Exception as e:
        csettings = None
        status = ''
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'avatar': UserProfile.objects.get(user=request.user).avatar,
            'user_type': FacultyProfile.objects.get(faculty=request.user).get_faculty_type_display,
            'status': status,
            'viewtype': 'home',
            'title': 'Home',
            'announcements': announcements,
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


#===================================================
#                   AJAX_COMPONENTS
#===================================================
@login_required
def ajax_save(request):
    if request.is_ajax() and request.method == 'POST':
        viewtype = request.POST.get('viewtype')
        dict = request.POST.dict()
        pprint(dict)
        data = {}
        data['state'] = ''
        data['data'] = []

        # try:
        if viewtype == 'settings': # site_settings_save for querying
            school_year = dict['data[school_year]']
            sem = dict['data[sem]']

            current = Setting.objects.get(school_year=school_year,semester=sem)
            if int(dict['data[firstSection]']) != 0:
                current.first_sections = int(dict['data[firstSection]'])
                current.first_curriculum = Curriculum.objects.get(pk=dict['data[firstCurriculum]'])
            else:
                current.first_sections = 0
                current.first_curriculum = None

            if int(dict['data[secondSection]']) != 0:
                current.second_sections = int(dict['data[secondSection]'])
                current.second_curriculum = Curriculum.objects.get(pk=dict['data[secondCurriculum]'])
            else:
                current.second_sections = 0
                current.second_curriculum = None

            if int(dict['data[thirdSection]']) != 0:
                current.third_sections = int(dict['data[thirdSection]'])
                current.third_curriculum = Curriculum.objects.get(pk=dict['data[thirdCurriculum]'])
            else:
                current.third_sections = 0
                current.third_curriculum = None


            if int(dict['data[fourthSection]']) != 0:
                current.fourth_sections = int(dict['data[fourthSection]'])
                current.fourth_curriculum = Curriculum.objects.get(pk=dict['data[fourthCurriculum]'])
            else:
                current.fourth_sections = 0
                current.fourth_curriculum = None

            if int(dict['data[fifthSection]']) != 0:
                current.fifth_sections = int(dict['data[fifthSection]'])
                current.fifth_curriculum = Curriculum.objects.get(pk=dict['data[fifthCurriculum]'])
            else:
                current.fifth_sections = 0
                current.fifth_curriculum = None

            current.save()
            data['state'] = 'SUCCESS'
        # except Exception as e:
        #     print(e)
        #     data['state'] = str(e)

        data = json.dumps(data)
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponse({}, content_type='application/json')

#===================================================
#                   LOAD MANAGER
#===================================================
@login_required
def load_manager_list(request):
    cs = None
    psched = None
    status = "No Offering"
    try:
        settings = Setting.objects.get(current=True)
        status =  settings.get_status_display
        if PreferredSchedule.objects.filter(user=request.user,school_year=settings.school_year,semester=settings.semester).exists() and status:
            cs = True
            psched = PreferredSchedule.objects.get(user=request.user,school_year=settings.school_year,semester=settings.semester)
        else:
            cs = False
            psched = ""
    except:
        settings = None


    context = {
        'avatar': UserProfile.objects.get(user=request.user).avatar,
        'user_type': FacultyProfile.objects.get(faculty=request.user).get_faculty_type_display,
        'csetting': settings,
        'title': 'LOAD MANAGER',
        'status': status,
        'viewtype': 'load-manager',
        'submission': cs,
        'psubj': psched,
    }
    return render(request, 'load_manager/components/faculty-load/list.html', context)

@login_required
def load_manager_tables(request):
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
    settings = Setting.objects.get(current=True)
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
        os.system('cls')
        selected = request.POST.getlist('timedays')
        subjects = request.POST.getlist('psubjects')
        print(subjects)
        setting = Setting.objects.get(current=True)
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
## ============= CURRICULUM
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def curriculum_settings(request):
    curriculums = Curriculum.objects.all()
    context = {
        'avatar': UserProfile.objects.get(user=request.user).avatar,
        'user_type': FacultyProfile.objects.get(faculty=request.user).get_faculty_type_display,
        'viewtype': 'curriculum',
        'curriculums': curriculums,
    }

    return render(request, 'load_manager/components/chairperson/curriculum.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def curriculum_subject_edit(request, pk):

    curriculum = Curriculum.objects.get(pk=pk)
    subjects = Subject.objects.filter(curriculum=curriculum).order_by('-offered', 'subject_code')

    if request.method == 'GET':
        context = {
            'avatar': UserProfile.objects.get(user=request.user).avatar,
            'user_type': FacultyProfile.objects.get(faculty=request.user).get_faculty_type_display,
            'curriculum': curriculum,
            'subjects': subjects,
        }
        return render(request, 'load_manager/components/chairperson/curriculum-edit.html', context)
    # if request.method == 'POST':
    #     for subject in subjects:
    #         # subject.minor_flag = request.POST.get('%s-minor-flag' % (subject.subject_code))
    #         # subject.thesis_flag = request.POST.get('%s-thesis-flag' % (subject.subject_code))
    #         # subject.save()
    #         if request.POST.get('%s-minor-flag' % (subject.subject_code)):
    #             subject.minor_flag = True
    #             subject.thesis_flag = False
    #             print('%s Offered' % (subject.subject_code))
    #         else:
    #             subject.minor_flag = False

    #         a = request.POST.get('room-STAT 2053')
    #         print(a)
    #         subject.save()
    #     return redirect('settings-curriculum')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def curriculum_subject_table(request, pk):
    import json
    from pprint import pprint
    subjects = Subject.objects.filter(curriculum__pk=pk)
    data = []
    for subject in subjects:
        if subject.offered:
            offered = "Offered"
        else:
            offered = "Not offered"
        x = {"fields":{"subject-id": subject.pk,
                       "subject-code": subject.subject_code,
                       "subject-name": subject.subject_name,
                       "subject-yl": subject.year_level,
                       "subject-sem": subject.get_semester_display(),
                       "subject-offered": offered,
                       "subject-room": subject.get_room_category_display(),
             }
        }
        data.append(x)
    data = json.dumps(data)
    pprint(data)
    return HttpResponse(data, content_type='application/json')

    return HttpResponse(subjects)

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def curriculum_settings_subject(request):
    import json
    from pprint import pprint
    # subjects = Subject.objects.filter(curriculum=pk)
    curriculums = Curriculum.objects.all()
    data = []
    for curriculum in curriculums:
        x = {"fields":{"curriculum-name":curriculum.curriculum,
                       "curriculum-description":curriculum.description,
                       "curriculum-pk":curriculum.pk,
             }
        }
        data.append(x)
    data = json.dumps(data)
    pprint(data)
    return HttpResponse(data, content_type='application/json')

    return HttpResponse(subjects)

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def curriculum_settings_table(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        type = request.POST.get('type')
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

#  ============= SITE SETTINGS
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def site_settings(request):
    curriculum = Curriculum.objects.all()
    try:
        current_settings = Setting.objects.get(current=True)
    except:
        current_settings = None
    context = {
        'avatar': UserProfile.objects.get(user=request.user).avatar,
        'user_type': FacultyProfile.objects.get(faculty=request.user).get_faculty_type_display,
        'title': 'Settings',
        'viewtype': 'settings',
        'csetting': current_settings,
        'sem_status': SEMESTER_STATUS(),
        'school_year': SchoolYear.objects.all(),
        'semesters': SEMESTERS(),
        'curriculum': curriculum,
    }
    # settings = Setting.objects.get_or_create()

    return render(request, 'load_manager/components/chairperson/settings/index.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def site_settings_view(request,pk):
    curriculum = Curriculum.objects.all()

    context = {
        'viewtype': 'settings',
        'school_year': SchoolYear.objects.all(),
        'semesters': SEMESTERS(),
        'curriculum': curriculum,
    }
    # settings = Setting.objects.get_or_create()

    # return render(request, , context)
    return HttpResponse(pk, content_type='application/json')
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def site_settings_table(request):
    settings = Setting.objects.all()
    data = []
    for setting in settings:
        x = {"fields":{"id":setting.pk,
                       "sy":[setting.pk,str(setting.school_year)],
                       "semester":setting.get_semester_display(),
                       "status":setting.current
             }
        }
        data.append(x)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def site_settings_save(request,viewtype,sy,sem):
    context = {
        'viewtype': 'settings',
        'title': 'Semester Settings',
        'message': f'Do you want to save setting for SY[<b>{SchoolYear.objects.get(pk=sy)}</b>] <b>{Setting.objects.get(current=True).get_semester_display()}</b>',
        'query':"""{
                    "school_year": """+str(sy)+""",
                    "sem":  """+str(sem)+""",
                    // FIRST YEAR
                     "firstSection" : $('input[name= "first-section"]').val(),
                     "firstCurriculum": function(data){
                         if($('select[name= "first-select"]').is(':disabled')){
                             return 'disabled'
                         } else {
                           return $('select[name= "first-select"] :selected').val()
                         }
                     },
                     // SECOND YEAR
                     "secondSection": $('input[name= "second-section"]').val(),
                     "secondCurriculum": function(data){
                         if($('select[name= "second-select"]').is(':disabled')){
                             return 'disabled'
                         } else {
                           return $('select[name= "second-select"] :selected').val()
                         }
                     },
                     // THIRD YEAR
                     "thirdSection": $('input[name= "third-section"]').val(),
                     "thirdCurriculum": function(data){
                         if($('select[name= "third-select"]').is(':disabled')){
                             return 'disabled'
                         } else {
                           return $('select[name= "third-select"] :selected').val()
                         }
                     },
                     // FOURTH YEAR
                     "fourthSection": $('input[name= "fourth-section"]').val(),
                     "fourthCurriculum": function(data){
                         if($('select[name= "fourth-select"]').is(':disabled')){
                             return 'disabled'
                         } else {
                           return $('select[name= "fourth-select"] :selected').val()
                         }
                     },

                     // fifth YEAR
                     "fifthSection": $('input[name= "fifth-section"]').val(),
                     "fifthCurriculum": function(data){
                         if($('select[name= "fifth-select"]').is(':disabled')){
                             return 'disabled'
                         } else {
                           return $('select[name= "fifth-select"] :selected').val()
                         }
                     },

                 }
                 """
    }
    return render(request, 'load_manager/components/modals/save.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def site_settings_open(request,sy,sem):
    csettings = Setting.objects.get(current=True)
    context = {
        'title': 'Open Encoding',
        'school_year': csettings.school_year,
        'semester': csettings.get_semester_display,
        'message': '',
    }
    return render(request, 'load_manager/components/chairperson/settings/modals/encoding-open.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def site_settings_opened_table(request):
    if request.is_ajax():
        cs = Setting.objects.get(current=True)
        preferreds = PreferredSchedule.objects.all().filter(school_year=cs.school_year, semester=cs.semester)
        data = []
        for pf in preferreds:
            x = {"fields":{"id":pf.pk,
                           "faculty":f'{pf.user.first_name} {pf.user.last_name}',
                 }
            }
            data.append(x)
        data = json.dumps(data)
        return HttpResponse(data, content_type='application/json')
# ============= SECTION OFFERING
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def section_offering(request):
    try:
        current_settings = Setting.objects.get(current=True)
    except Exception as e:
        current_settings = None

    context = {
        'avatar': UserProfile.objects.get(user=request.user).avatar,
        'user_type': FacultyProfile.objects.get(faculty=request.user).get_faculty_type_display,
        'title': 'Section Offering',
        'viewtype': 'section-offering',
        'settings': current_settings,
    }
    # settings = Setting.objects.get_or_create()

    return render(request, 'load_manager/components/chairperson/section-offering/index.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def section_offering_table(request):
    import json
    from pprint import pprint
    settings = Setting.objects.get(current=True)
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

    secOffs = SectionOffering.objects.filter(school_year=sy, semester=semester)

    data = []
    for secOff in secOffs:
        if secOff.professor:
            prof = str(secOff.professor.first_name + ' ' + secOff.professor.last_name)
        else:
            prof = "Empty"
        x = {"fields":{"id": secOff.pk,
                       "secOff-subject": str(secOff.subject.subject_name),
                       "secOff-section": str(secOff.block_section),
                       "secOff-type": secOff.get_service_flag_display(),
                       "secOff-prof": prof,
             }
        }
        data.append(x)
    data = json.dumps(data)
    pprint(data)
    return HttpResponse(data, content_type='application/json')

## FACULTY LOAD
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def faculty_load(request):
    try:
        current_settings = Setting.objects.get(current=True)
    except Exception as e:
        current_settings = None

    context = {
        'avatar': UserProfile.objects.get(user=request.user).avatar,
        'user_type': FacultyProfile.objects.get(faculty=request.user).get_faculty_type_display,
        'title': 'Section Offering',
        'viewtype': 'faculty-load',
        'settings': current_settings,
    }
    # settings = Setting.objects.get_or_create()

    return render(request, 'load_manager/components/chairperson/faculty-load.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def faculty_load_table(request):
    import json
    from pprint import pprint
    settings = Setting.objects.get(current=True)
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

    fls = FacultyLoad.objects.filter(subject__school_year=sy, subject__semester=semester)

    data = []
    for fl in fls:
        if fl.subject.professor:
            prof = str(fl.subject.professor.first_name + ' ' + fl.subject.professor.last_name)
        else:
            prof = "Empty"
        if fl.load_schedule:
            time = str(fl.load_schedule.preferred_time)
            sched = str(fl.load_schedule.preferred_time.all().first()) + ' to ' + str(fl.load_schedule.preferred_time.all().last()) + ' Room ' + str(fl.load_schedule.room.room_name)
        else:
            time = "Empty"
            sched = "Empty"
        if fl.load_schedule:
            room = str(fl.load_schedule.room)
        else:
            room = "Empty"


        x = {"fields":{"fl-id": fl.pk,
                       "fl-subject": str(fl.subject.subject.subject_name),
                       "fl-section": str(fl.subject.block_section),
                       "fl-type": fl.get_load_category_display(),
                       "fl-sched": sched,
                       "fl-prof": prof,
             }
        }
        data.append(x)
    data = json.dumps(data)
    pprint(data)
    return HttpResponse(data, content_type='application/json')

from django.core.files.storage import FileSystemStorage
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def curriculum_upload(request):

    if request.method == 'GET':
        context = {}
        return render(request, 'load_manager/components/chairperson/curriculum-upload.html', context)

    elif request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        #uploaded_file_url = (str(settings.BASE_DIR) + str(fs.url(filename))).replace('/', '\\') #if deployed on windows
        uploaded_file_url = (str(settings.BASE_DIR) + str(fs.url(filename))) #.replace('/', '\\') #if deployed on linux
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
                        if strcode.startswith('BSCOE') or strcode.startswith('COEN'):
                            new_subj.offered= True
                        new_subj.save()

                    print(f'{strcode} - {strdesc} - {strlab} - {strlec}')

        return redirect('settings-curriculum')

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

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def generate_semester_offering(request):
    settings = Setting.objects.get(current=True)
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

        # first_s = Subject.objects.filter(year_level=1, semester=semester, curriculum=first_c).filter(
        #     Q(subject_code__startswith='COEN')|Q(subject_code__startswith='BSCOE'))
    if settings.first_sections:
        first_c = Curriculum.objects.get(curriculum=settings.first_curriculum.curriculum)
        first_s = Subject.objects.filter(year_level=1, semester=semester, curriculum=first_c, offered=True)
        first_sl = list(first_s)
        print(first_sl)
        semOff.subject.add(*first_sl)
    if settings.second_sections:
        second_c = Curriculum.objects.get(curriculum=settings.second_curriculum.curriculum)
        second_s = Subject.objects.filter(year_level=2, semester=semester, curriculum=first_c, offered=True)
        second_sl = list(second_s)
        print(second_sl)
        semOff.subject.add(*second_sl)
    if settings.third_sections:
        third_c = Curriculum.objects.get(curriculum=settings.third_curriculum.curriculum)
        third_s = Subject.objects.filter(year_level=3, semester=semester, curriculum=first_c, offered=True)
        third_sl = list(third_s)
        print(third_sl)
        semOff.subject.add(*third_sl)
    if settings.fourth_sections:
        fourth_c = Curriculum.objects.get(curriculum=settings.fourth_curriculum.curriculum)
        fourth_s = Subject.objects.filter(year_level=4, semester=semester, curriculum=first_c, offered=True)
        fourth_sl = list(fourth_s)
        print(fourth_sl)
        semOff.subject.add(*fourth_sl)
    if settings.fifth_sections:
        fifth_c = Curriculum.objects.get(curriculum=settings.fifth_curriculum.curriculum)
        fifth_s = Subject.objects.filter(year_level=5, semester=semester, curriculum=first_c, offered=True)
        fifth_sl = list(fifth_s)
        print(fifth_sl)
        semOff.subject.add(*fifth_sl)

    semOff.save()

    context = {
        'subjects': semOff.subject.all(),
    }

    return redirect('generate_section_offering')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def generate_section_offering(request):
    settings = Setting.objects.get(current=True)
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
        # fifth_count = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=5).count()
        fifth_count = int(settings.fifth_sections)
    except:
        fifth_count = 0
    print(f'fifth year - {fifth_count}')
    try:
        #fourth_count = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=4).count()
        fourth_count = int(settings.fourth_sections)
    except:
        fourth_count = 0
    print(f'fourth year - {fourth_count}')
    try:
        #third_count = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=3).count()
        third_count = int(settings.third_sections)
    except:
        third_count = 0
    print(f'third year - {third_count}')
    try:
        #second_count = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=2).count()
        second_count = int(settings.second_sections)
    except:
        second_count = 0
    print(f'second year - {second_count}')
    try:
        #first_count = BlockSection.objects.filter(school_year=sy, semester=semester, year_level=1).count()
        first_count = int(settings.first_sections)
    except:
        first_count = 0
    print(f'first year - {first_count}')

    # generate block sections
    for i in range(fifth_count):
        try:
            bs = BlockSection.objects.get(school_year=sy, semester=semester, year_level=5, section=str(int(i+1)))
        except BlockSection.DoesNotExist:
            bs = BlockSection(school_year=sy, semester=semester, year_level=5, section=str(int(i+1)))
            bs.save()
        print(bs)

    for i in range(fourth_count):
        try:
            bs = BlockSection.objects.get(school_year=sy, semester=semester, year_level=4, section=str(int(i+1)))
        except BlockSection.DoesNotExist:
            bs = BlockSection(school_year=sy, semester=semester, year_level=4, section=str(int(i+1)))
            bs.save()
        print(bs)

    for i in range(third_count):
        try:
            bs = BlockSection.objects.get(school_year=sy, semester=semester, year_level=3, section=str(int(i+1)))
        except BlockSection.DoesNotExist:
            bs = BlockSection(school_year=sy, semester=semester, year_level=3, section=str(int(i+1)))
            bs.save()
        print(bs)

    for i in range(second_count):
        try:
            bs = BlockSection.objects.get(school_year=sy, semester=semester, year_level=2, section=str(int(i+1)))
        except BlockSection.DoesNotExist:
            bs = BlockSection(school_year=sy, semester=semester, year_level=2, section=str(int(i+1)))
            bs.save()
        print(bs)

    for i in range(first_count):
        try:
            bs = BlockSection.objects.get(school_year=sy, semester=semester, year_level=1, section=str(int(i+1)))
        except BlockSection.DoesNotExist:
            bs = BlockSection(school_year=sy, semester=semester, year_level=1, section=str(int(i+1)))
            bs.save()
        print(bs)

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

    return redirect('generate_faculty_load')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def allocate_section_offering(request):
    settings = Setting.objects.get(current=True)
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

    # Loop through subjects from section offering; based on settings'
    #   semester and sy; descending by year level; ascending subject code.
    secOff_qs = SectionOffering.objects.filter(school_year=sy, semester=semester).exclude(professor__isnull=False).order_by('-subject__year_level', 'subject__subject_code')

    for secOff in secOff_qs:
        print(secOff)
    # Query all prof; filtered by preferred subject (this subject);
    #   first come first serve on list maximum section count of this.subject.year_level
        user_list = []
        prefScheds = PreferredSchedule.objects.filter(school_year=sy, semester=semester, preferred_subject=secOff.subject)
        for prefSched in prefScheds:
            user_list.append(prefSched.user)
        # print(user_list)
    # Loop through filtered prof; descending based on Faculty Priority Rule
        profs = FacultyProfile.objects.filter(faculty__in=user_list).order_by('-faculty_type')
        if profs:
            for prof in profs:
                print(f'{prof.faculty} prefers {secOff.subject}')
    # If prof already allocated to this.subject, next.
                secOff_prof_exists = SectionOffering.objects.filter(school_year=sy, semester=semester, professor=prof.faculty, subject=secOff.subject)
    # If prof has no remaining hours, next.
                secOff_prof_qs = SectionOffering.objects.filter(school_year=sy, semester=semester, professor=prof.faculty)
                allowed_hours = prof.regular_hours + prof.part_time_hours
                allocated_hours = 0
                subject_hours = secOff.subject.lab_hours + secOff.subject.lec_hours
                print(secOff_prof_qs)
                for secOff_prof in secOff_prof_qs:
                    allocated_hours += secOff_prof.subject.lec_hours + secOff_prof.subject.lec_hours

                print(f'{prof.faculty} total of {allocated_hours} allocated hours')
                print(f'{prof.faculty} total of {allowed_hours} allowed hours')

                if secOff_prof_exists:
                    print(f'{prof.faculty} already assigned to subject {secOff.subject} - {subject_hours}hrs')
                else:
                    print(f'{prof.faculty} not assigned to subject {secOff.subject} - {subject_hours}hrs')
                    if allocated_hours + subject_hours <= allowed_hours:
                        print(f'{prof.faculty} allocated to {secOff.subject}')
                        secOff.professor = prof.faculty
                        secOff.save()
                        print(secOff.professor)
                        break
                    else:
                        print(f'{prof.faculty} not allocated to {secOff.subject}')



    # Allocation subject to prof; first come, first serve.
    return redirect('section-offering')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def generate_faculty_load(request):
    settings = Setting.objects.get(current=True)
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

    # Loop through section offering
    secOffs = SectionOffering.objects.filter(school_year=sy, semester=semester)
    # Check secOff.subject lab hours, lec hours
    for secOff in secOffs:
        lab_hours = secOff.subject.lab_hours
        lec_hours = secOff.subject.lec_hours
        print(f'{secOff.subject} {lab_hours} + {lec_hours}')
    # If > 0 lab hours and >= 5 lab hrs - lab1 labhrs//2+1 lab2 lab//hrs+2 - lab1
    # elif >0 lab hours < 5 lab1 - labhrs
    # create FL
        if lab_hours > 0 and lab_hours >= 5:
            try:
                facload = FacultyLoad.objects.get(subject=secOff, load_category=0)
            except FacultyLoad.DoesNotExist:
                facload = FacultyLoad(subject=secOff, load_category=0)
                facload.save()
            print(facload)
            try:
                facload = FacultyLoad.objects.get(subject=secOff, load_category=1)
            except FacultyLoad.DoesNotExist:
                facload = FacultyLoad(subject=secOff, load_category=1)
                facload.save()
            print(facload)
        elif lab_hours > 0 and lab_hours < 5:
            try:
                facload = FacultyLoad.objects.get(subject=secOff, load_category=0)
            except FacultyLoad.DoesNotExist:
                facload = FacultyLoad(subject=secOff, load_category=0)
                facload.save()
            print(facload)
    # If > 0 lec hours and >= 5 lec hrs - lec1 lechrs//2+1 lec2 lec//hrs+2 - lec1
    # elif >0 lec hours < 5 lec1 - lechrs
        if lec_hours > 0 and lec_hours >= 5:
            try:
                facload = FacultyLoad.objects.get(subject=secOff, load_category=2)
            except FacultyLoad.DoesNotExist:
                facload = FacultyLoad(subject=secOff, load_category=2)
                facload.save()
            print(facload)
            try:
                facload = FacultyLoad.objects.get(subject=secOff, load_category=3)
            except FacultyLoad.DoesNotExist:
                facload = FacultyLoad(subject=secOff, load_category=3)
                facload.save()
            print(facload)
        elif lec_hours > 0 and lec_hours < 5:
            try:
                facload = FacultyLoad.objects.get(subject=secOff, load_category=2)
            except FacultyLoad.DoesNotExist:
                facload = FacultyLoad(subject=secOff, load_category=2)
                facload.save()
            print(facload)
    # create FL
    settings.status = 1
    settings.save()
    return redirect('settings')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def allocate_faculty_load(request):
    settings = Setting.objects.get(current=True)
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

    # loop through prof, descending faculty type
    profs = FacultyProfile.objects.all().order_by('-faculty_type')
    for prof in profs:
    # loop through section offerings assigned to faculty
        print(f'FACULTY {prof.faculty}')
        # fls = FacultyLoad.objects.filter(subject__professor=prof.faculty, load_schedule=None)
        secOffs = SectionOffering.objects.filter(professor=prof.faculty, school_year=sy, semester=semester)
        for secOff in secOffs:
            print(secOff)
            fls = FacultyLoad.objects.filter(subject__professor=prof.faculty, load_schedule=None, subject=secOff)
            for fl in fls:

                print(fl)
                #check hours
                #check if lab or lec
                #if > 5, split // + 1, if < 5, full. allocate 3 hours first, then 2 hours
                lab_hours = fl.subject.subject.lab_hours
                lec_hours = fl.subject.subject.lec_hours
                if lab_hours >= 5:
                    if lab_hours % 2:
                        lab1 = lab_hours//2
                        lab2 = lab_hours//2 - 1
                    else:
                        lab1 = lab_hours//2
                        lab2 = lab_hours//2
                    if fl.load_category == 0:
                        labhr = lab1
                    elif fl.load_category == 1:
                        labhr = lab2
                elif lab_hours < 5:
                    lab1 = lab_hours
                    if fl.load_category == 0:
                        labhr = lab1

                if lec_hours >= 5:
                    if lec_hours % 2:
                        lec1 = lec_hours//2
                        lec2 = lec_hours//2 - 1
                    else:
                        lec1 = lec_hours//2
                        lec2 = lec_hours//2
                    if fl.load_category == 2:
                        lechr = lec1
                    elif fl.load_category == 3:
                        lechr = lec2
                elif lec_hours < 5:
                    lec1 = lec_hours
                    if fl.load_category == 2:
                        lechr = lec1

                if fl.load_category == 0 or fl.load_category == 1:
                    subjhr = labhr
                elif fl.load_category == 2 or fl.load_category == 3:
                    subjhr = lechr
                print(f'{subjhr} hrs')
                divisions = int(subjhr/0.5)
                print(str(divisions) + ' divisions')
                # check prof preferred time
                prof_preferred_time = PreferredSchedule.objects.get(user=prof.faculty, school_year=sy, semester=semester).preferred_time.all()
                ppt_list = list(prof_preferred_time)
                # print(f'PPT LIST {ppt_list}')
                prof_assigned_time = FacultyLoad.objects.filter(subject__professor=prof.faculty)
                pat_list = []
                for pat in prof_assigned_time:
                    if pat.load_schedule:
                        pat_list += list(pat.load_schedule.preferred_time.all())
                print(f'ASSIGNED LOAD {prof_assigned_time}')
                print(f'ALREADY TIME {pat_list}')
                # fls_allocated = FacultyLoad.objects.filter(load_schedule__isnull=False)
                rooms = Room.objects.filter(room_category=secOff.subject.room_category)
                print(f'ROOMS {rooms}')
                for room in rooms:
                    print(f'ROOM {room.room_name}')

                    fl_room_occupants = FacultyLoad.objects.filter(load_schedule__room=room)
                    print(f'ROOM OCCUPANTS {fl_room_occupants}')
                    check_sched = []
                    for fl_room_occupant in fl_room_occupants:
                        check_sched += list(fl_room_occupant.load_schedule.preferred_time.all())
                    print(f'TIME OCCUPIED {check_sched}')
                    for i in range(5):
                        for j in range(26-divisions):
                            check_time = []
                            check_time_ids = []
                            for k in range(divisions):
                                check_time.append(PreferredTime.objects.get(select_time=j+k, select_day=i))
                                check_time_ids.append(PreferredTime.objects.get(select_time=j+k, select_day=i).pk)
                            # print(f'{bool([item for item in check_time if item in check_sched])}')
                            # print(f'{not bool(all(item in ppt_list for item in check_time))}')
                            # print(f'{not bool([item for item in check_time if item in pat_list])}')
                            # print(f'ct {check_time}')
                            # print(f'cs {check_sched}')
                            # print(f'pat {pat_list}')
                            if bool([item for item in check_time if item in check_sched]) or not bool(all(item in ppt_list for item in check_time)) or bool([item for item in check_time if item in pat_list]):
                                print("J next loop")
                            else:
                                print(f'{bool([item for item in check_time if item in check_sched])} - {not bool(all(item in ppt_list for item in check_time))} - {bool([item for item in check_time if item in pat_list])}')
                                break #break for j
                        if bool([item for item in check_time if item in check_sched]) or not bool(all(item in ppt_list for item in check_time)) or bool([item for item in check_time if item in pat_list]):
                            print("I next loop")
                        else:
                            print(f'{bool([item for item in check_time if item in check_sched])} - {not bool(all(item in ppt_list for item in check_time))} - {bool([item for item in check_time if item in pat_list])}')
                            break #break for i
                    if bool([item for item in check_time if item in check_sched]) or not bool(all(item in ppt_list for item in check_time)) or bool([item for item in check_time if item in pat_list]):
                        print("R next loop")
                    else:
                        print(f'{bool([item for item in check_time if item in check_sched])} - {not bool(all(item in ppt_list for item in check_time))} - {bool([item for item in check_time if item in pat_list])}')
                        break #break for room
                if bool([item for item in check_time if item in check_sched]) or not bool(all(item in ppt_list for item in check_time)) or bool([item for item in check_time if item in pat_list]):
                    print("FL next loop")
                else:
                    print(f'{bool([item for item in check_time if item in check_sched])} - {not bool(all(item in ppt_list for item in check_time))} - {bool([item for item in check_time if item in pat_list])}')

                    fl_preferred_time = PreferredTime.objects.filter(pk__in=check_time_ids)
                    load_schedule = LoadSchedule.objects.filter(room=room, preferred_time__in=fl_preferred_time).first()
                    if not load_schedule:
                        print('doesnt exists')
                        load_schedule = LoadSchedule(room=room)
                        load_schedule.save()
                        load_schedule.preferred_time.set(fl_preferred_time)
                        load_schedule.save()
                        load_schedule = LoadSchedule.objects.filter(room=room, preferred_time__in=fl_preferred_time).first()
                    print(load_schedule)
                    fl.load_schedule = load_schedule
                    fl.save()
                    print(f'ASSIGNED TO ROOM - {room.room_name} - {i} -  SCHEDULE - {check_time}')
                    # try:
                    #     fl_next = fls[1]
                    # except IndexError:
                    #     fl_next = False
                    # if i == 0 and fl_next:
                    #     print(f'{fl_next} load is thursday')
                    # elif i == 1:
                    #     print('next load is friday')
                    # elif i == 2:
                    #     print('next load is saturday')

                    break #break for fl

    return HttpResponse(secOffs)

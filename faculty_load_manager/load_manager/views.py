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
from django.utils import timezone

def home_view(request):
    next = request.GET.get('next')
    status = ''
    announcements = None
    try:
        csettings = Setting.objects.get(current=True)
        status = csettings.get_status_display
        announcements = Announcement.objects.order_by('-created')[:5]
    except Exception as e:
        csettings = None
        status = ''
        accouncements = None
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
            psched = None
    except:
        settings = None

    context = {
        'avatar': UserProfile.objects.get(user=request.user).avatar,
        'user_type': FacultyProfile.objects.get(faculty=request.user).get_faculty_type_display,
        'preferred_time': psched,
        'times': PreferredTime.TIME_SELECT,
        'days': DAY_OF_THE_WEEK,
        'csetting': settings,
        'title': 'LOAD MANAGER',
        'status': status,
        'viewtype': 'load-manager',
        'submission': cs,
        'psubj': psched,
    }

    if psched != None:
        context['ptimes']=psched.preferred_time.all().values_list('select_day','select_time')
    else:
        context['ptimes']=None

    import os
    os.system('cls')
    print('PTIME: ',context['ptimes'])
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
                       "status": str(load.get_status_display()),
                       "user_id": request.user.pk,
             }
        }
        data.append(x)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
@login_required
def load_manager_create(request):
    faculty_type = FacultyProfile.objects.get(faculty=request.user).faculty_type
    settings = Setting.objects.get(current=True)
    time_schedules = PreferredTime.objects.all()
    current_user = request.user
    subjs = SemesterOffering.objects.get(school_year=settings.school_year,semester=settings.semester).subject.all()
    import os
    os.system('cls')
    print(faculty_type)
    context = {
        'title': 'LOAD MANAGER | FORM',
        'viewtype': 'load-manager',
        'user': request.user,
        'avatar': UserProfile.objects.get(user=request.user).avatar,
        'user_type': FacultyProfile.objects.get(faculty=request.user).get_faculty_type_display,
        'subjects': subjs,
        'type': faculty_type,
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
    semester = str(Setting.objects.get(current=True).semester)
    sy = get_school_year()

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
    semester = str(Setting.objects.get(current=True).semester)
    sy = get_school_year()

    fls = FacultyLoad.objects.filter(subject__school_year=sy, subject__semester=semester)

    data = []
    for fl in fls:
        if fl.subject.professor:
            prof = str(fl.subject.professor.first_name + ' ' + fl.subject.professor.last_name)
        else:
            prof = "Empty"
        if fl.load_schedule and fl.load_schedule.room:
            time = str(fl.load_schedule.preferred_time)
            sched = str(fl.load_schedule.preferred_time.all().first()) + ' to ' + str(fl.load_schedule.preferred_time.all().last()) + ' Room ' + str(fl.load_schedule.room.room_name)
            room = str(fl.load_schedule.room)
        elif fl.load_schedule and not fl.load_schedule.room:
            time = str(fl.load_schedule.preferred_time)
            sched = str(fl.load_schedule.preferred_time.all().first()) + ' to ' + str(fl.load_schedule.preferred_time.all().last()) + ' Room Empty'
            room = "Empty"
        else:
            time = "Empty"
            sched = "Empty"
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

## ROOMSM
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def rooms(request):
    try:
        current_settings = Setting.objects.get(current=True)
    except Exception as e:
        current_settings = None

    context = {
        'avatar': UserProfile.objects.get(user=request.user).avatar,
        'user_type': FacultyProfile.objects.get(faculty=request.user).get_faculty_type_display,
        'title': 'Rooms',
        'viewtype': 'rooms',
        'settings': current_settings,
    }
    # settings = Setting.objects.get_or_create()

    return render(request, 'load_manager/components/chairperson/room/index.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def room_table(request):
    import json
    from pprint import pprint

    # try:
    #     settings = Setting.objects.get(current=True)
    #     semester = str(Setting.objects.get(current=True).semester)
    # except Exception as e:
    #     response = JsonResponse({"error": str(e),
    #                              "message":"SETTINGS THIS SEMESTER DOES NOT EXIST"})
    #     response.status_code = 403 # To announce that the user isn't allowed to publish
    #     return response
    #
    # sy = get_school_year()
    #
    #
    # fls = FacultyLoad.objects.filter(subject__school_year=sy, subject__semester=semester)
    rooms = Room.objects.all()
    data = []
    for room in rooms:
        x = {"fields":{"id": room.pk,
                       "name": room.room_name,
                       "category": room.get_room_category_display(),
             }
        }
        data.append(x)
    data = json.dumps(data)
    pprint(data)
    return HttpResponse(data, content_type='application/json')

## SECTIONS
## ROOMSM
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def sections(request):
    try:
        current_settings = Setting.objects.get(current=True)
        curr_sy = current_settings.school_year
    except Exception as e:
        current_settings = None
        curr_sy = None
    context = {
        'avatar': UserProfile.objects.get(user=request.user).avatar,
        'user_type': FacultyProfile.objects.get(faculty=request.user).get_faculty_type_display,
        'title': 'Sections',
        'curr_sy': curr_sy,
        'viewtype': 'sections',
        'settings': current_settings,
    }

    return render(request, 'load_manager/components/chairperson/sections/index.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def section_table(request, q):
    settings = Setting.objects.get(current=True)
    semester = str(settings.semester)
    start_year = str(settings.school_year.start_year)
    end_year = str(settings.school_year.end_year)
    rooms = Room.objects.all()

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

    current_sections = BlockSection.objects.filter(school_year=sy, semester=semester)

    data = []
    for section in current_sections:
        x = {"fields":{"id": section.pk,
                       "year-lvl": section.year_level,
                       "section": section.section,
             }
        }
        data.append(x)
    data = json.dumps(data)
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
    semester = str(Setting.objects.get(current=True).semester)
    sy = get_school_year()

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
    semester = str(Setting.objects.get(current=True).semester)
    sy = get_school_year()

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

    # generate block sections and bs_preferredsched
    for i in range(fifth_count):
        try:
            bs = BlockSection.objects.get(school_year=sy, semester=semester, year_level=5, section=str(int(i+1)))
        except BlockSection.DoesNotExist:
            bs = BlockSection(school_year=sy, semester=semester, year_level=5, section=str(int(i+1)))
            bs.save()
        print(bs)
        try:
            bs_ps = Ys_PreferredSchedule.objects.get(block_section=bs)
        except Ys_PreferredSchedule.DoesNotExist:
            bs_ps = Ys_PreferredSchedule(block_section=bs)
            bs_ps.save()
        print(bs_ps)

    for i in range(fourth_count):
        try:
            bs = BlockSection.objects.get(school_year=sy, semester=semester, year_level=4, section=str(int(i+1)))
        except BlockSection.DoesNotExist:
            bs = BlockSection(school_year=sy, semester=semester, year_level=4, section=str(int(i+1)))
            bs.save()
        print(bs)
        try:
            bs_ps = Ys_PreferredSchedule.objects.get(block_section=bs)
        except Ys_PreferredSchedule.DoesNotExist:
            bs_ps = Ys_PreferredSchedule(block_section=bs)
            bs_ps.save()
        print(bs_ps)

    for i in range(third_count):
        try:
            bs = BlockSection.objects.get(school_year=sy, semester=semester, year_level=3, section=str(int(i+1)))
        except BlockSection.DoesNotExist:
            bs = BlockSection(school_year=sy, semester=semester, year_level=3, section=str(int(i+1)))
            bs.save()
        print(bs)
        try:
            bs_ps = Ys_PreferredSchedule.objects.get(block_section=bs)
        except Ys_PreferredSchedule.DoesNotExist:
            bs_ps = Ys_PreferredSchedule(block_section=bs)
            bs_ps.save()
        print(bs_ps)

    for i in range(second_count):
        try:
            bs = BlockSection.objects.get(school_year=sy, semester=semester, year_level=2, section=str(int(i+1)))
        except BlockSection.DoesNotExist:
            bs = BlockSection(school_year=sy, semester=semester, year_level=2, section=str(int(i+1)))
            bs.save()
        print(bs)
        try:
            bs_ps = Ys_PreferredSchedule.objects.get(block_section=bs)
        except Ys_PreferredSchedule.DoesNotExist:
            bs_ps = Ys_PreferredSchedule(block_section=bs)
            bs_ps.save()
        print(bs_ps)

    for i in range(first_count):
        try:
            bs = BlockSection.objects.get(school_year=sy, semester=semester, year_level=1, section=str(int(i+1)))
        except BlockSection.DoesNotExist:
            bs = BlockSection(school_year=sy, semester=semester, year_level=1, section=str(int(i+1)))
            bs.save()
        print(bs)
        try:
            bs_ps = Ys_PreferredSchedule.objects.get(block_section=bs)
        except Ys_PreferredSchedule.DoesNotExist:
            bs_ps = Ys_PreferredSchedule(block_section=bs)
            bs_ps.save()
        print(bs_ps)

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
def generate_faculty_load(request):
    settings = Setting.objects.get(current=True)
    semester = str(Setting.objects.get(current=True).semester)
    sy = get_school_year()

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

def get_school_year():
    settings = Setting.objects.get(current=True)
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

    return sy

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def sched_faculty_load(request):
    settings = Setting.objects.get(current=True)
    sy = get_school_year()
    semester = str(Setting.objects.get(current=True).semester)

    ## Loop through section offering, this will consist of 2 faculty loads
    ## Based on settings' semester and sy, descending by year level, ascending subject code
    secOff_qs = SectionOffering.objects.filter(school_year=sy, semester=semester).exclude(professor__isnull=False).order_by('-subject__year_level', 'subject__subject_code')
    for secOff in secOff_qs:
        print('=====START=====')
        print(secOff)
        fls = FacultyLoad.objects.filter(subject=secOff, load_schedule=None)
        if fls:
            print(f'FLS {fls.count()}')
    ## Get first faculty load
            # try:
            #     first_fl = FacultyLoad.objects.get(subject=secOff)
            #     second_fl = None
            # except Exception as e:
            first_fl = fls[0]
            try:
                second_fl = fls[1]
            except Exception as e:
                second_fl = None
            print(f'FIRST {first_fl}')

        ## Check if lab, lecture, or elecs_lab and how many hours.
            lab_hours = first_fl.subject.subject.lab_hours
            lec_hours = first_fl.subject.subject.lec_hours
            if lab_hours >= 5:
                if lab_hours % 2:
                    lab1 = lab_hours//2
                    lab2 = lab_hours//2 - 1
                else:
                    lab1 = lab_hours//2
                    lab2 = lab_hours//2
                if first_fl.load_category == 0:
                    labhr = lab1
                elif first_fl.load_category == 1:
                    labhr = lab2
            elif lab_hours < 5:
                lab1 = lab_hours
                if first_fl.load_category == 0:
                    labhr = lab1

            if lec_hours >= 5:
                if lec_hours % 2:
                    lec1 = lec_hours//2
                    lec2 = lec_hours//2 - 1
                else:
                    lec1 = lec_hours//2
                    lec2 = lec_hours//2
                if first_fl.load_category == 2:
                    lechr = lec1
                elif first_fl.load_category == 3:
                    lechr = lec2
            elif lec_hours < 5:
                lec1 = lec_hours
                if first_fl.load_category == 2:
                    lechr = lec1

            if first_fl.load_category == 0 or first_fl.load_category == 1:
                subjhr = labhr
            elif first_fl.load_category == 2 or first_fl.load_category == 3:
                subjhr = lechr
            print(f'{subjhr} hrs')
            divisions = int(subjhr/0.5)
            print(str(divisions) + ' divisions')

        ## Loop though time slots. Check if available for section and suits section's preferred sched. Check if same subject is parallel
            section_preferred_time = Ys_PreferredSchedule.objects.get(block_section=secOff.block_section).preferred_time.all()
            spt_list = list(section_preferred_time)
            #print(f'SPT LIST {spt_list}')

            section_assigned_load = FacultyLoad.objects.filter(subject__block_section=secOff.block_section)
            sal_list = []
            for sal in section_assigned_load:
                if sal.load_schedule:
                    sal_list += list(sal.load_schedule.preferred_time.all())
            #print(f'SECTION ASSIGNED LOAD {section_assigned_load}')
            #print(f'SECTION ALREADY TIME {sal_list}')

            same_subjects = FacultyLoad.objects.filter(subject__subject=secOff.subject)
            ss_assigned_time_list = []
            for same_subj in same_subjects:
                if same_subj.load_schedule:
                    ss_assigned_time_list += list(same_subj.load_schedule.preferred_time.all())
            #print(f'SAME SUBJECT TIMES {ss_assigned_time_list}')

            for i in range(6):
                for j in range(27-divisions):
                    check_time = []
                    check_time_ids = []
                    for k in range(divisions):
                        check_time.append(PreferredTime.objects.get(select_time=j+k, select_day=i))
                        check_time_ids.append(PreferredTime.objects.get(select_time=j+k, select_day=i).pk)
                    if bool([item for item in check_time if item in ss_assigned_time_list]) or not bool(all(item in spt_list for item in check_time)) or bool([item for item in check_time if item in sal_list]):
                        print("J next loop")
                    else:
                        print(f'{bool([item for item in check_time if item in ss_assigned_time_list])} - {not bool(all(item in spt_list for item in check_time))} - {bool([item for item in check_time if item in sal_list])}')
                        break #break for j
                if bool([item for item in check_time if item in ss_assigned_time_list]) or not bool(all(item in spt_list for item in check_time)) or bool([item for item in check_time if item in sal_list]):
                    if i == 5:
                        print('No Sched')
                        check_time_ids = []
                    else:
                        print("I next loop")
                else:
                    print(f'{bool([item for item in check_time if item in ss_assigned_time_list])} - {not bool(all(item in spt_list for item in check_time))} - {bool([item for item in check_time if item in sal_list])}')
                    break #break for i

            fl_assigned_time = PreferredTime.objects.filter(pk__in=check_time_ids)
            load_schedule = LoadSchedule(room=None)
            load_schedule.save()
            load_schedule.preferred_time.set(fl_assigned_time)
            load_schedule.save()
            first_fl.load_schedule = load_schedule
            first_fl.save()
            print(load_schedule)
            print(f'LOAD ASSIGNED TIME {list(fl_assigned_time)}')

        ## Allocate LoadSchedule time
        ## Loop through LoadSchedule (room + timeslot) and select available room
            if fl_assigned_time:
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

                    if bool([item for item in list(fl_assigned_time) if item in check_sched]):
                        print('NEXT ROOM')
                    else:
                        print(f'{bool([item for item in list(fl_assigned_time) if item in check_sched])}')
                        load = first_fl.load_schedule
                        load.room = room
                        load.save()
                        print(f'ASSIGNED TO ROOM {room.room_name}')
                        break


        ## Get second faculty load and consider mon-thurs tues-fri wed-sat pairing (this should be strict to ys_preferred sched as well)
            if second_fl and fl_assigned_time:
                print(f'SECOND {second_fl}')

        ## Check if lab, lecture, or elecs_lab and how many hours.
                lab_hours = second_fl.subject.subject.lab_hours
                lec_hours = second_fl.subject.subject.lec_hours
                if lab_hours >= 5:
                    if lab_hours % 2:
                        lab1 = lab_hours//2
                        lab2 = lab_hours//2 - 1
                    else:
                        lab1 = lab_hours//2
                        lab2 = lab_hours//2
                    if second_fl.load_category == 0:
                        labhr = lab1
                    elif second_fl.load_category == 1:
                        labhr = lab2
                elif lab_hours < 5:
                    lab1 = lab_hours
                    if second_fl.load_category == 0:
                        labhr = lab1

                if lec_hours >= 5:
                    if lec_hours % 2:
                        lec1 = lec_hours//2
                        lec2 = lec_hours//2 - 1
                    else:
                        lec1 = lec_hours//2
                        lec2 = lec_hours//2
                    if second_fl.load_category == 2:
                        lechr = lec1
                    elif second_fl.load_category == 3:
                        lechr = lec2
                elif lec_hours < 5:
                    lec1 = lec_hours
                    if second_fl.load_category == 2:
                        lechr = lec1

                if second_fl.load_category == 0 or second_fl.load_category == 1:
                    subjhr = labhr
                elif second_fl.load_category == 2 or second_fl.load_category == 3:
                    subjhr = lechr
                print(f'{subjhr} hrs')
                divisions = int(subjhr/0.5)
                print(str(divisions) + ' divisions')

                second_fl_day = fl_assigned_time[0].select_day
                x = 0
                if second_fl_day == 0:
                    x = 3
                elif second_fl_day == 1 or second_fl_day == 3:
                    x = 4
                elif second_fl_day == 2 or second_fl_day == 4:
                    x = 5
                elif second_fl_day == 6:
                    x = 6
                #print(f'2nd FL day {x}')

            ## Loop though time slots. Check if available for section and suits section's preferred sched. Check if same subject is parallel
                for i in range(x, 6):
                    for j in range(27-divisions):
                        check_time = []
                        check_time_ids = []
                        for k in range(divisions):
                            check_time.append(PreferredTime.objects.get(select_time=j+k, select_day=i))
                            check_time_ids.append(PreferredTime.objects.get(select_time=j+k, select_day=i).pk)
                        if bool([item for item in check_time if item in ss_assigned_time_list]) or not bool(all(item in spt_list for item in check_time)) or bool([item for item in check_time if item in sal_list]):
                            print("J next loop")
                        else:
                            print(f'{bool([item for item in check_time if item in ss_assigned_time_list])} - {not bool(all(item in spt_list for item in check_time))} - {bool([item for item in check_time if item in sal_list])}')
                            break #break for j
                    if bool([item for item in check_time if item in ss_assigned_time_list]) or not bool(all(item in spt_list for item in check_time)) or bool([item for item in check_time if item in sal_list]):
                        print("I next loop")
                    else:
                        print(f'{bool([item for item in check_time if item in ss_assigned_time_list])} - {not bool(all(item in spt_list for item in check_time))} - {bool([item for item in check_time if item in sal_list])}')
                        break #break for i

            ## Allocate LoadSchedule time
                fl2_assigned_time = PreferredTime.objects.filter(pk__in=check_time_ids)
                load_schedule2 = LoadSchedule(room=None)
                load_schedule2.save()
                load_schedule2.preferred_time.set(fl2_assigned_time)
                load_schedule2.save()
                second_fl.load_schedule = load_schedule2
                second_fl.save()
                print(load_schedule2)
                print(f'LOAD ASSIGNED TIME {fl2_assigned_time}')

            ## Loop through LoadSchedule (room + timeslot) and select available room
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

                    if bool([item for item in list(fl2_assigned_time) if item in check_sched]):
                        print('NEXT ROOM')
                    else:
                        print(f'{bool([item for item in list(fl2_assigned_time) if item in check_sched])}')
                        load = second_fl.load_schedule
                        load.room = room
                        load.save()
                        print(f'ASSIGNED TO ROOM {room.room_name}')
                        break
        else:
            print(f'{secOff} already assigned')
        print('=====END=====')
    return redirect('faculty-load')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def assign_prof(request):
    settings = Setting.objects.get(current=True)
    sy = get_school_year()
    semester = str(Setting.objects.get(current=True).semester)

    ## Query section offering based on settings, excluding already assigned
    ## and sy descending by year level and ascending by subject code, then query faculty load
    secOff_qs =  SectionOffering.objects.filter(school_year=sy, semester=semester).exclude(professor__isnull=False).order_by('-subject__year_level', 'subject__subject_code')
    for secOff in secOff_qs:
        fls = FacultyLoad.objects.filter(subject=secOff)
        subject_hours = secOff.subject.lab_hours + secOff.subject.lec_hours
        #print(f'FLS {fls}')

    ## Create list of preferred times of section offering
        fls_list = []
        for fl in fls:
            if fl.load_schedule:
                fls_list += list(fl.load_schedule.preferred_time.all())

    ## Query profs who prefers this section offering
    ## - first come first server descending based on Faculty Priority Rule
        user_list = []
        prefScheds = PreferredSchedule.objects.filter(school_year=sy, semester=semester, preferred_subject=secOff.subject)
        for prefSched in prefScheds:
            user_list.append(prefSched.user)

        profs = FacultyProfile.objects.filter(faculty__in=user_list).order_by('-faculty_type')
        if profs:
            for prof in profs:
                print("===START===")
                print(f"SECTION OFFERING {secOff}")
                #print(f'FLS_LIST {fls_list}')
                print(f'PROFESSOR {prof.faculty} PREFERS {secOff.subject}')

    ## Check if already allocated to this type of subject, next if yes.
                secOff_prof_exists = SectionOffering.objects.filter(school_year=sy, semester=semester, professor=prof.faculty, subject=secOff.subject)

    ## Check prof remaining hours, next if no remaining hours.
                secOff_prof_qs = SectionOffering.objects.filter(school_year=sy, semester=semester, professor=prof.faculty)
                allowed_hours = prof.regular_hours + prof.part_time_hours
                allocated_hours = 0
                subject_hours = secOff.subject.lab_hours + secOff.subject.lec_hours
                #print(secOff_prof_qs)
                for secOff_prof in secOff_prof_qs:
                    allocated_hours += secOff_prof.subject.lec_hours + secOff_prof.subject.lec_hours

                print(f'{prof.faculty} total of {allocated_hours} allocated hours')
                print(f'{prof.faculty} total of {allowed_hours} allowed hours')

    ## Check if prof preferred sched matches section offering's faculty load's preferred sched and if it is available
                prof_preferred_time = PreferredSchedule.objects.get(user=prof.faculty, school_year=sy, semester=semester).preferred_time.all()
                ppt_list = list(prof_preferred_time)
                #print(f'PROF PREFERRED {prof_preferred_time}')
                prof_assigned_load = FacultyLoad.objects.filter(subject__professor=prof.faculty)
                pat_list = []
                for pat in prof_assigned_load:
                    if pat.load_schedule:
                        pat_list += list(pat.load_schedule.preferred_time.all())
                #print(f'ALREADY TIME {pat_list}')
                #print(f'{bool([item for item in fls_list if item in ppt_list])}')
                print(f'{not bool(secOff_prof_exists)} - {bool(allocated_hours + subject_hours <= allowed_hours)} - {bool(all(item in ppt_list for item in fls_list))} - {not bool([item for item in fls_list if item in pat_list])}' )
                if not bool(secOff_prof_exists) and bool(allocated_hours + subject_hours <= allowed_hours) and bool(all(item in ppt_list for item in fls_list)) and not bool([item for item in fls_list if item in pat_list]):
                    secOff.professor = prof.faculty
                    secOff.save()
                    print(f'ALLOCATED TO {prof.faculty}')
                    break #break for prof
                else:
                    print ('NEXT PROF')
                print("===END===")
        #here
        announcement_message = f'Faculty load has now been allocated for {sy} - {semester}'
        new_announcement = Announcement(title="Faculty Load", message=announcement_message)
        new_announcement.save()
    return redirect('faculty-load')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def clear_fl(request):
    fls = FacultyLoad.objects.all()
    for fl in fls:
        fl.load_schedule = None
        fl.save()
        print(fl.load_schedule)
    return HttpResponse("cleared sched")

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def clear_prof(request):
    secOffs = SectionOffering.objects.all()
    for secOff in secOffs:
        secOff.professor = None
        secOff.save()
        print(secOff.professor)
    return HttpResponse("cleared prof")
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
    settings.status = 2
    settings.save()
    return redirect('section-offering')

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
                prof_assigned_load = FacultyLoad.objects.filter(subject__professor=prof.faculty)
                pat_list = []
                for pat in prof_assigned_load:
                    if pat.load_schedule:
                        pat_list += list(pat.load_schedule.preferred_time.all())
                print(f'ASSIGNED LOAD {prof_assigned_load}')
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
                    for i in range(6):
                        for j in range(27-divisions):
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

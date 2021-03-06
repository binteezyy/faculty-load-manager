from django.urls import path, include
from . import views
from users.views import *
from . import model_views
urlpatterns = [
    path('', views.home_view, name='home'),

    # AJAX MODULES
    path('ajax/save', views.ajax_save, name='ajax-save'),

    # MODEL CRUDS
    # ANNOUCEMENT
    path('create/annoucement', model_views.AnnouncementCreateView.as_view(),
         name='create-annoucement'),
    path('delete/annoucement/<int:pk>',
         model_views.AnnouncementDeleteView.as_view(), name='delete-annoucement'),
    # SETTINGS
    path('create/user-management/users/create',
         user_pool_management_create, name='chairperson-upm-user-create'),
    path('read/user/<int:pk>', model_views.UserReadView.as_view(), name='read-user'),
    path('update/user/<int:pk>',
         model_views.UserUpdateView.as_view(), name='update-user'),
    path('delete/user/<int:pk>',
         model_views.UserDeleteView.as_view(), name='delete-user'),

    # SECTION OFFERING
    path('create/section-offerings', model_views.SectionOfferingCreateView.as_view(),
         name='create-section-offering'),
    path('read/section-offering/<int:pk>',
         model_views.SectionOfferingReadView.as_view(), name='read-section-offering'),
    path('update/section-offering/<int:pk>',
         model_views.SectionOfferingUpdateView.as_view(), name='update-section-offering'),
    path('delete/section-offering/<int:pk>',
         model_views.SectionOfferingDeleteView.as_view(), name='delete-section-offering'),

    # MODAL URLS
    path('read/settings/faculty-prefer/<int:pk>',
         model_views.SettingsFacultyPreferReadView.as_view(), name='read-settings-'),
    path('delete/settings/faculty-prefer/<int:pk>',
         model_views.SettingsFacultyPreferDeleteView.as_view(), name='delete-settings'),
    path('read/settings/faculty-load-alloted/<int:pk>',
         model_views.SettingsFacultyLoadAllotedReadView.as_view(), name='read-load-alloted'),

    # FACULTY LOAD
    path('create/faculty-loads', model_views.FacultyLoadCreateView.as_view(),
         name='create-faculty-load'),
    path('read/faculty-load/<int:pk>',
         model_views.FacultyLoadReadView.as_view(), name='read-faculty-load'),
    path('update/faculty-load/<int:pk>',
         model_views.FacultyLoadUpdateView.as_view(), name='update-faculty-load'),
    path('delete/faculty-load/<int:pk>',
         model_views.FacultyLoadDeleteView.as_view(), name='delete-faculty-load'),

    # SEMESTER OFFERING
    # CURRICULUM
    path('update/curriculum/<int:pk>',
         model_views.CurriculumUpdateView.as_view(), name='update-curriculum'),
    path('delete/curriculum/<int:pk>',
         model_views.CurriculumDeleteView.as_view(), name='delete-curriculum'),
    # SUBJECT
    path('create/curriculum/subjects', model_views.SubjectCreateView.as_view(),
         name='create-curriculum-subject'),
    path('read/curriculum/subject/<int:pk>',
         model_views.SubjectReadView.as_view(), name='read-curriculum-subject'),
    path('update/curriculum/subject/<int:pk>',
         model_views.SubjectUpdateView.as_view(), name='update-curriculum-subject'),
    path('delete/curriculum/subject/<int:pk>',
         model_views.SubjectDeleteView.as_view(), name='delete-curriculum-subject'),

    # ROOM
    path('create/room', model_views.RoomCreateView.as_view(),
         name='create-room'),
    path('read/room/<int:pk>', model_views.RoomReadView.as_view(), name='read-room'),
    path('delete/room/<int:pk>',
         model_views.RoomDeleteView.as_view(), name='delete-room'),
    path('update/room/<int:pk>',
         model_views.RoomUpdateView.as_view(), name='update-room'),

    # SETTINGS
    path('create/settings', model_views.SettingsCreateView.as_view(),
         name='create-settings'),
    path('read/settings/<int:pk>',
         model_views.SettingsReadView.as_view(), name='read-settings'),
    path('update/settings/<int:pk>',
         model_views.SettingsUpdateView.as_view(), name='update-settings'),
    path('delete/settings/<int:pk>',
         model_views.SettingsDeleteView.as_view(), name='delete-settings'),

    # LOAD MANAGER
    path('load-manager/', views.load_manager_list, name='load-manager-list'),
    path('load-manager/create/', views.load_manager_create,
         name='load-manager-create'),
    path('load-manager/form/', views.load_manager_create,
         name='load-manager-form'),
    path('load-manager/my-history/', views.load_manager_tables,
         name='load-manager-history-tables'),



    # CHAIRPERSON VIEW
    # CURRICULUM
    path('chairperson/curriculum/', views.curriculum_settings,
         name='settings-curriculum'),
    path('chairperson/curriculum/<int:pk>',
         views.curriculum_subject_edit, name='curriculum-edit'),
    path('chairperson/curriculum/subject-table/<int:pk>',
         views.curriculum_subject_table, name='chairperson-curriculum-subject-table'),
    path('chairperson/curriculum/upload', views.curriculum_upload,
         name='settings-curriculum-upload'),
    path('chairperson/curriculum/table', views.curriculum_settings_subject,
         name='chairperson-curriculum-table'),

    # SETTINGS
    path('chairperson/settings/', views.site_settings, name='settings'),
    path('chairperson/settings/<int:pk>',
         views.site_settings_view, name='settings'),
    path('chairperson/settings/table',
         views.site_settings_table, name='settings-table'),
    path('chairperson/settings/save/<str:viewtype>/<int:sy>/<int:sem>', views.site_settings_save,
         name='chairperson-settings-save'),
    path('chairperson/settings/open-sem/<int:sy>/<int:sem>/', views.site_settings_open,
         name='chairperson-settings-open'),
    path('chairperson/settings/open-sem/table/', views.site_settings_opened_table,
         name='chairperson-settings-open-table'),
    # SECTION OFFERING
    path('chairperson/section-offering/',
         views.section_offering, name='section-offering'),
    path('chairperson/section-offering/table', views.section_offering_table,
         name='chairperson-section-offering-table'),
    # ROOM
    path('chairperson/settings/room/', views.rooms, name='room'),
    path('chairperson/settings/room/table',
         views.room_table, name='room-table'),

    # SECTIONS
    path('chairperson/settings/sections/', views.sections, name='sections'),
    path('chairperson/settings/sections/table/<str:q>',
         views.section_table, name='sections-table'),
    path('read/sections/<int:pk>', model_views.SectionsReadView.as_view(),
         name='read-block-section'),
    path('create/sections', model_views.SectionCreateView.as_view(),
         name='create-block-section'),
    path('delete/section/<int:pk>',
         model_views.SectionsDeleteView.as_view(), name='delete-section'),
    path('update/section/<int:pk>',
         model_views.SectionsUpdateView, name='update-section'),
    path('update/section/<int:pk>/weekdays',
         model_views.SectionsUpdateAll, name='update-section-weekdays'),
    # FACULTY LOAD
    path('chairperson/faculty-load/', views.faculty_load, name='faculty-load'),
    path('chairperson/faculty-load/table', views.faculty_load_table,
         name='chairperson-faculty-load-table'),
    # USER MANAGEMENT
    path('chairperson/user-management/',
         user_pool_management, name='chairperson-upm'),
    path('chairperson/user-management/users/table',
         user_pool_mangement_table, name='chairperson-upm-user-table'),


    # FUNCTIONS
    path('parse/', views.parse_view, name='parse_view'),
    path('generate/', views.generate_semester_offering,
         name='generate_semester_offering'),
    path('so/', views.generate_section_offering,
         name='generate_section_offering'),
    path('fl/', views.generate_faculty_load, name='generate_faculty_load'),
    path('chairperson/clear-fl', views.clear_fl, name='clear-fl'),
    path('chairperson/clear-prof', views.clear_prof, name='clear-prof'),

    # ALGO
    path('chairperson/sched-fl', views.sched_faculty_load,
         name='sched-faculty-load'),
    path('chairperson/assign-prof', views.assign_prof, name='assign-prof'),
    path('chairperson/allocate-so', views.allocate_section_offering,
         name='allocate_section_offering'),
    path('chairperson/allocate-fl', views.allocate_faculty_load,
         name='allocation_faculty_load'),

]

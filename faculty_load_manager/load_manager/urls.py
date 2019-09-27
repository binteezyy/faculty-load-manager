from django.urls import path, include
from . import views
from users.views import *
urlpatterns = [
    path('', views.home_view, name='home'),

    # LOAD MANAGER
    path('my/load-manager/', views.load_manager_list, name='load-manager-list'),
    path('my/load-manager/create/', views.load_manager_create,
         name='load-manager-create'),
    path('my/load-manager/form/', views.load_manager_create,
         name='load-manager-form'),
    path('load-manager/my-history/', views.load_manager_tables,
         name='load-manager-history-tables'),

    # TEST URLS
    path('ss', views.ss, name='ss'),

    # CHAIRPERSON VIEW
    path('settings/', views.site_settings, name='settings'),
    path('settings/change/', views.change_settings, name='settings-change'),
    path('settings/curriculum/', views.curriculum_settings,
         name='settings-curriculum'),
    path('settings/curriculum/<int:pk>/subjects/',
         views.curriculum_settings_subject, name='settings-curriculum-subjects'),
    path('settings/curriculum/upload', views.curriculum_upload,
         name='settings-curriculum-upload'),
    path('chairperson/user-management/',
         user_pool_management, name='chairperson-upm'),
    path('chairperson/user-management/users/table',
         user_pool_mangement_table, name='chairperson-upm-user-table'),
    path('chairperson/user-management/users/create',
         user_pool_management_create, name='chairperson-upm-user-create'),
    # AJAX
    path('parse/', views.parse_view, name='parse_view'),
    path('generate/', views.generate_semester_offering,
         name='generate_semester_offering'),
    path('so/', views.generate_section_offering,
         name='generate_section_offering'),
]

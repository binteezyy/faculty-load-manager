from django.urls import path, include
from . import views
from users.views import *
urlpatterns = [
    path('', views.home_view, name='home'),

    # AJAX MODULES
    path('ajax/save', views.ajax_save, name='ajax-save'),
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
    ## SETTINGS
    path('chairperson/settings/', views.site_settings, name='settings'),
    path('chairperson/settings/<int:pk>', views.site_settings_view, name='settings'),
    path('chairperson/settings/table', views.site_settings_table, name='settings-table'),
    path('chairperson/settings/save/<str:viewtype>/<int:sy>/<int:sem>', views.site_settings_save,
        name='chairperson-settings-save'),
    path('chairperson/curriculum/', views.curriculum_settings,
         name='settings-curriculum'),
    path('chairperson/curriculum/<int:name>',
         views.curriculum_edit, name='curriculum-edit'),
    path('chairperson/curriculum/upload', views.curriculum_upload,
         name='settings-curriculum-upload'),
    path('chairperson/curriculum/table', views.curriculum_settings_subject,
         name='chairperson-curriculum-table'),
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

     #ALGO
     path('chairperson/generate-load', views.generate_load, name='generate_load')
]

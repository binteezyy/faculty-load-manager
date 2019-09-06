from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),

    # LOAD MANAGER
    path('load-manager/', views.load_manager_list, name='load-manager-list'),
    path('load-manager/create/',views.load_manager_create, name='load-manager-create'),
    path('load-manager/form/', views.load_manager_create, name='load-manager-form'),

    ## TEST URLS
    path('ss', views.ss, name='ss'),

    ## SETTINGS
    path('settings/', views.site_settings, name='settings'),
    path('settings/change/', views.change_settings, name='settings-change'),

    ## AJAX
    path('parse/', views.parse_view, name='parse_view'),
    path('generate/', views.generate_semester_offering, name='generate_semester_offering'),
]

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('settings/', views.site_settings, name='settings'),

    # LOAD MANAGER
    path('load-manager/', views.load_manager_list, name='load-manager-list'),
    path('load-manager/create/',views.pload_view, name='load-manager-create'),
    path('pload/', views.pload_view, name='pload'),

    ## TEST URLS
    path('ss', views.ss, name='ss'),

    ## AJAX
    path('settings/change/', views.change_settings, name='change-settings'),
    path('parse/', views.parse_view, name='parse_view'),
    path('generate/', views.generate_semester_offering, name='generate_semester_offering'),
    path('so/', views.generate_section_offering, name='generate_section_offering'),
]

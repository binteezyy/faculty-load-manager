from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('pload/', views.pload_view, name='pload'),
    path('settings/', views.site_settings, name='settings'),
    ## TEST URLS
    path('ss', views.ss, name='ss'),

    ## AJAX
    path('settings/change/', views.change_settings, name='change-settings'),
    path('parse/', views.parse_view, name='parse_view'),
]

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('pload/', views.pload_view, name='pload'),

    ## TEST URLS
    path('ss', views.ss, name='ss'),
]

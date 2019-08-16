from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('pload/', views.pload_view, name='pload'),
    path('logout/', views.logout_view, name='logout'),


    ## TEST URLS
    path('ss', views.ss, name='ss'),
]

from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('account/<int:pk>', views.user_profile,
         name='user-profile'),

    path('account/password-reset/', views.PasswordResetView.as_view(),
         name='password-reset'),
    path('account/password-reset/', views.PasswordResetDoneView.as_view(),
         name='password-reset-done'),
    path('reset/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
 # accounts/password_reset/done/ [name='password_reset_done']


]

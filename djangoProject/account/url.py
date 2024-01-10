from django.urls import path, include

from account import views

urlpatterns = [
    path('login', views.login_views, name='login'),
    path('logout', views.logout_views, name='logout'),
    path('singUp', views.signup_views, name='signUp'),
    path('profile', views.profile, name='profile'),
]

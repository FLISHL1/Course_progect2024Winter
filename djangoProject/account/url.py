from django.urls import path, include

from account import views

urlpatterns = [
    path('auth', views.auth, name='auth'),
    path('logout', views.exit, name='logout'),
]

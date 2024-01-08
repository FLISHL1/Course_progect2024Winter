from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from account.sign_up_form import SignUpForm


# Create your views here.
def login_views(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('')
        else:
            return HttpResponseRedirect("login")
    else:
        return render(request, 'account/login.html', {'title': "Авторизация"})

def signup_views(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if User.objects.filter(username=username).exists():
            return render(request, 'account/login.html', {'title': "Регистрация", "message": f"Пользователь с логином {username} уже существует"})
        else:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return HttpResponseRedirect("login")

    else:
        return render(request, 'account/login.html', {'title': "Регистрация"})


@login_required
def logout_views(request):
    logout(request)
    return HttpResponseRedirect("login")

def test(request):
    return render(request, 'main.html')

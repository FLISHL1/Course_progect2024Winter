from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib import messages  # import messages


# Create your views here.
def login_views(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"Добро пожаловать {user.first_name}!")
            return redirect('mainPage')
        else:
            messages.info(request, f"Такой пользователь не найден!")
            return redirect("login")
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
            messages.info(request, f"Пользователь с логином {username} уже существует")
            return redirect('signUp')
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
    messages.info(request, "Выход выполнен успешно")
    return redirect("login")


@login_required
def profile(request):
    if request.method == 'POST':
        username = request.POST['login']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user = request.user
        if old_password != "":
            if user.check_password(old_password):
                if new_password != "":
                    user.set_password(new_password)
            else:
                messages.info(request, "Старый пароль не совпадает!")

        if email != "":
            user.email = email

        user.username = username
        user.first_name = first_name
        user.last_name = last_name

        user.save()

    return render(request, 'account/profile.html')


def index(request):
    return render(request, 'main.html')



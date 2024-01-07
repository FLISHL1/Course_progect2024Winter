from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def auth(request):
    if (request.method == 'POST'):
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Успех")
        else:
            return HttpResponseRedirect("auth")
    else:
        return render(request, 'account/auth.html')


@login_required
def exit(request):
    logout(request)
    return HttpResponseRedirect("auth")


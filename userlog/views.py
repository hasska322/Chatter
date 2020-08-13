import re
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def index(request):
    return render(request, 'index.html', )


def signin(request):
    return render(request, 'sigin.html')


def create(request):
    if request.method == "POST":
        password = request.POST.get("pass")
        re_pass = request.POST.get("re_pass")
        if not re.match(r'[A-Za-z0-9]{8,16}', password):
            messages.error(request, 'Пароль должен состоять из букв и цифр')
            return redirect('/signup')
        if password == re_pass:
            email = request.POST.get('email')
            try:
                if User.objects.get(username=email):
                    messages.error(request, 'Данный email уже используется')
                    return redirect('/signup')
            except User.DoesNotExist:
                pass
            user = User.objects.create_user(email, email, password)
            user.first_name = request.POST.get('name')
            user.last_name = request.POST.get('company')
            user.save()
        else:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('/signup')
    return HttpResponseRedirect("/chat")


def logging(request):
    username = request.POST['email']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/chat/')
        else:
            messages.error(request, 'Ваш аккаунт не активирован!')
            return redirect('/signin/')
    else:
        try:
            if User.objects.get(username=username):
                messages.error(request, 'Не верный пароль!')
                return redirect('/signup')
        except User.DoesNotExist:
            pass
        messages.error(request, 'Пользователь не существует!')
        return redirect('/signin/')


def logout_view(request):
    logout(request)
    return redirect('/signin/')


def chat(request):
    if request.user.is_authenticated:
        return render(request, 'chat.html')
    else:
        return redirect('/signin/')

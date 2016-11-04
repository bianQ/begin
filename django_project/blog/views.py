from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib import auth

from .models import User
from .forms import LoginForm, RegisterForm

@login_required()
def index(request):
    return render(request, 'blog/index.html')

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return render(request, 'blog/index.html')
            else:
                login_error = 'Username or password error'
                return render(request, 'blog/login.html', {'form': form, 'login_error':login_error})

@login_required()
def logout(request):
    return render(request, 'blog/index.html')

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'blog/register.html', {'form':form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            if password1 == password2:
                user = User(username=username, password=password1, email=email)
                user.save()
                return render(request, 'blog/login.html')
            else :
                register_error = '两次输入密码不匹配'
                return render(request, 'blog/register.html', {'form':form, 'register_error':register_error})
        else:
            return render(request, 'blog/register.html', {'form': form})
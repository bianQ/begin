from django.shortcuts import render, HttpResponseRedirect

# Create your views here.

from django.contrib import auth
from django.contrib.auth.models import User
from django.conf import settings as django_setting
from django.core.mail import send_mail

from .forms import LoginForm, RegisterForm, PostForm, ConfirmEmailForm, NewPasswordForm
from .Token import token_confirm

def index(request):
    form = PostForm()
    return render(request, 'blog/index.html', {'form': form})

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
            if user :
                auth.login(request, user)
                return render(request, 'blog/index.html')
            else:
                login_error = 'Username or password error'
                return render(request, 'blog/login.html', {'form': form, 'login_error':login_error})
        else :
            return render(request, 'blog/login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/blog/')

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
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
                token = token_confirm.generate_validate_token(username)
                message = '''
                你好!

                感谢你的注册。
                你的登录邮箱为：{email}。请点击以下链接激活帐号：

                {domain}/blog/{active}/{token}

                （该链接在24小时内有效，24小时后需要重新注册）
                '''.format(email=email,domain=django_setting.DOMAIN,active='active',token=token)
                send_mail('激活账号', message, '15989490620@163.com', [email])
                return render(request, 'blog/message.html', {'message':'请登陆邮箱验证并激活账号'})
            else :
                register_error = '两次输入密码不匹配'
                return render(request, 'blog/register.html', {'form':form, 'register_error':register_error})
        else:
            return render(request, 'blog/register.html', {'form': form})

def profile(request, id):
    return render(request, 'blog/profile.html')

def active(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username)
        for user in users:
            if user.is_active == False:
                user.delete()
        return render(request, 'blog/message.html', {'message':'你访问的页面已失效，请重新注册', 'href':'/blog/register'})
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'blog/message.html', {'message':'用户不存在，请重新注册', 'href':'/blog/register'})
    user.is_active = True
    user.save()
    return render(request, 'blog/message.html', {'message':'验证成功，欢迎你的加入,赶紧登陆吧', 'href':'/blog/login'})

def getpassword(request):
    if request.method == 'GET':
        form = ConfirmEmailForm()
        return render(request, 'blog/getpassword.html', {'form': form})
    else:
        form = ConfirmEmailForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username, email=email):
                token = token_confirm.generate_validate_token(username)
                message = '''
                {username}，您好：

                    您最近提出了密码重设请求。要完成此过程，请点按以下链接。

                    {domain}/blog/{reset}/{token}

                    （该链接在24小时内有效，24小时后需要重新验证）
                '''.format(username=username, domain=django_setting.DOMAIN, reset='newpassword', token=token)
                send_mail('找回密码', message, '15989490620@163.com', [email])
                return render(request, 'blog/message.html', {'message': '邮件已发送，请登陆邮箱确认'})
            else :
                return render(request, 'blog/getpassword.html', {'form': form, 'message_error': '用户名或邮箱错误'})
        return render(request, 'blog/getpassword.html', {'form': form})

def changepassword(request):
    pass

def newpassword(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        return render(request, 'blog/message.html', {'message':'你访问的页面已失效，请重新验证'})
    if request.method == 'GET':
        form = NewPasswordForm()
        return render(request, 'blog/newpassword.html', {'form': form, 'username': username})
    else:
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                user = User.objects.get(username=username)
                user.password = password1
                user.save()
                return render(request, 'blog/message.html', {'message':'密码修改成功，赶紧登陆吧','href':'/blog/login'})
            else:
                return render(request, 'blog/newpassword.html', {'form':form, 'message':'两次输入密码不匹配'})
        return render(request, 'blog/newpassword.html', {'form':form})
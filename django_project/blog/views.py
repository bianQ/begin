from django.shortcuts import render, HttpResponseRedirect

# Create your views here.

from django.contrib import auth
from django.contrib.auth.models import User
from django.conf import settings as django_setting
from django.core.mail import send_mail

from .forms import LoginForm, RegisterForm
from .Token import token_confirm

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
            if user :
                auth.login(request, user)
                return render(request, 'blog/index.html')
            else:
                login_error = 'Username or password error'
                return render(request, 'blog/login.html', {'form': form, 'login_error':login_error})


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
            user.delete()
        return render(request, 'blog/message.html', {'message':'你访问的页面已失效，请重新注册'})
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'blog/message.html', {'message':'用户不存在，请重新注册'})
    user.is_active = True
    user.save()
    return render(request, 'blog/message.html', {'message':'验证成功，欢迎你的加入'})
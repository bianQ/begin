from django.shortcuts import render, HttpResponseRedirect, redirect

# Create your views here.

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Blog, UserProfile, Comment
from django.conf import settings as django_setting
from django.core.mail import send_mail

from .forms import LoginForm, RegisterForm, PostForm, ConfirmEmailForm, NewPasswordForm, CommentForm
from .Token import token_confirm

import requests, re

def index(request):
    posts = Blog.objects.order_by('-pub_date')[:6]
    return render(request, 'blog/index.html', {'posts':posts, 'lenth':len(posts)})

#登陆
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
                return render(request, 'blog/profile.html')
            else:
                login_error = 'Username or password error'
                return render(request, 'blog/login.html', {'form': form, 'login_error':login_error})
        else :
            return render(request, 'blog/login.html', {'form': form})

#注销
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/blog/')

#账号注册，并发送验证邮件
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
                userprofile = UserProfile.objects.create(user_id=user.id)
                userprofile.save()
                token = token_confirm.generate_validate_token(username)
                message = '''
                你好!

                感谢你的注册。
                你的登录邮箱为：{email}。请点击以下链接激活帐号：

                {domain}/blog/{active}/{token}

                （该链接在24小时内有效，24小时后需要重新注册）
                '''.format(email=email,domain=django_setting.DOMAIN,active='active',token=token)
                send_mail('激活账号', message, '15989490620@163.com', [email])
                return render(request, 'blog/message.html', {'message':'请登陆邮箱验证并激活账号', 'flag':False})
            else :
                register_error = '两次输入密码不匹配'
                return render(request, 'blog/register.html', {'form':form, 'register_error':register_error})
        else:
            return render(request, 'blog/register.html', {'form': form})

#用户资料页，待实现
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'blog/404.html')
    userprofile = user.userprofile_set.all().first()
    posts = user.blog_set.order_by('pub_date')[:5]
    return render(request, 'blog/profile.html',{'posts':posts, 'userprofile':userprofile})

#邮箱验证，通过则激活账号
def active(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username)
        for user in users:
            if user.is_active == False:
                user.delete()
        return render(request, 'blog/message.html', {'message':'你访问的页面已失效，请重新注册', 'flag':'重新注册', 'href':'/blog/register'})
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'blog/message.html', {'message':'用户不存在，请重新注册', 'flag':'重新注册', 'href':'/blog/register'})
    user.is_active = True
    user.save()
    return render(request, 'blog/message.html', {'message':'验证成功，欢迎你的加入,赶紧登陆吧', 'flag':'立即登陆', 'href':'/blog/login'})

#找回密码，若username和email验证通过，则向所提供的邮箱发送验证邮件
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
                return render(request, 'blog/message.html', {'message': '邮件已发送，请登陆邮箱确认', 'flag':False})
            else :
                return render(request, 'blog/getpassword.html', {'form': form, 'message_error': '用户名或邮箱错误'})
        return render(request, 'blog/getpassword.html', {'form': form})

#修改密码，待实现
def changepassword(request):
    pass

#密码重置，验证token
def newpassword(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        return render(request, 'blog/message.html', {'message':'你访问的页面已失效，请重新验证', 'flag':'重新验证', 'href':'/blog/getpassword'})
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
                return render(request, 'blog/message.html', {'message':'密码修改成功，赶紧登陆吧','flag':'立即登陆', 'href':'/blog/login'})
            else:
                return render(request, 'blog/newpassword.html', {'form':form, 'message':'两次输入密码不匹配'})
        return render(request, 'blog/newpassword.html', {'form':form})

#博客详情页
def article(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return render(request, 'blog/404.html')
    try:
        commented = blog.comment_set.all().order_by('-pub_date')
    except Comment.DoesNotExist:
        commented = None
    if request.method == 'GET':
        form = CommentForm()
        blog.read += 1
        blog.save()
        return render(request, 'blog/article.html', {'blog':blog, 'form':form, 'comments':commented})
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['comment']
            profile_id = UserProfile.objects.get(user=request.user).id
            comment = Comment.objects.create(blog_id=id, user_id=request.user.id, profile_id=profile_id, body=body)
            comment.save()
            new_comment = blog.comment_set.all().order_by('-pub_date').order_by('-pub_date')
            return render(request, 'blog/article.html', {'blog':blog, 'form':form, 'comments':new_comment})
        return render(request, 'blog/article.html', {'blog': blog, 'form': form, 'comments':commented})

def createblog(request, username):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blog/createblog.html', {'form':form})
    else:
        user = User.objects.get(username=username)
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            profile_id = UserProfile.objects.get(user=user).id
            blog = Blog.objects.create(author_id=user.id, profile_id=profile_id, title=title, body=body)
            blog.save()
            return render(request, 'blog/article.html', {'blog':blog})
        return render(request, 'blog/createblog.html', {'form':form})

def getmap(request, location):
    ak = django_setting.BAIDU_MAP_KEY  #百度地图API key，自行申请
    url = 'http://api.map.baidu.com/geocoder/v2/?address={location}&output=json&ak={ak}' \
          '&callback=showLocation'.format(location=location, ak=ak)
    data = requests.get(url)
    x = re.findall('"lng":([0-9]+\.[0-9]+)', data.text)[0]
    y = re.findall('"lat":([0-9]+\.[0-9]+)', data.text)[0]
    map_url = 'http://map.baidu.com/?latlng={y},{x}' \
              '&title=我的位置&content={location}&output=html'.format(x=x, y=y, location=location)
    return redirect(map_url)
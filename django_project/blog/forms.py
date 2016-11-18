from django import forms
from django.core.exceptions import ValidationError

from .models import User

import re

#判断用户名有效性
def validators_username(username):
    if re.findall('^[A-Za-z][A-Za-z0-9_.]*$', username) == []:
        raise ValidationError('用户名只能包含字母大小写、数字、点及下划线且以字母开头')
    users = User.objects.filter(username=username)
    for user in users:
        if user:
            if user.is_active == False:
                user.delete()
            else:
                raise ValidationError('用户名已占用')

#判断邮箱有效性
def validators_email(email):
    users = User.objects.filter(email=email)
    for user in users:
        if user:
            if user.is_active == False:
                user.delete()
            else:
                raise ValidationError('邮箱已注册')

#判断邮箱是否存在，用于找回密码
def email_exist(email):
    if User.objects.filter(email=email) is None:
        raise ValidationError('邮箱不存在')

#判断用户名是否存在，用于找回密码
def username_exist(username):
    if User.objects.filter(username=username) is None:
        raise ValidationError('用户名不存在')

#登陆表单
class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'user-name', 'placeholder':'请输入用户名/邮箱/手机号'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'pass-word', 'placeholder':'请输入密码'}))

#注册表单
class RegisterForm(forms.Form):
    username = forms.CharField(label='', max_length=16, validators=[validators_username],
                               widget=forms.TextInput(attrs={'class':'user-name', 'placeholder':'请输入用户名'}))
    email = forms.EmailField(label='', validators=[validators_email],
                             widget=forms.TextInput(attrs={'class':'email', 'placeholder':'请输入邮箱'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'pass-word', 'placeholder':'请输入密码'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'pass-word', 'placeholder':'确认密码'}))

class PostForm(forms.Form):
    title = forms.CharField()
    body = forms.CharField()

#找回密码，验证表单
class ConfirmEmailForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=16, validators=[username_exist])
    email = forms.EmailField(label='邮 箱', validators=[email_exist])

#修改密码表单，待实现
class ChangePasswordForm(forms.Form):
    pass

#重置密码表单
class NewPasswordForm(forms.Form):
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'pass-word', 'placeholder':'请输入新密码'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'pass-word', 'placeholder':'确认密码'}))
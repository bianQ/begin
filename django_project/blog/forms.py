from django import forms
from django.core.exceptions import ValidationError

from .models import User

import re

def validators_username(username):
    if re.findall('^[A-Za-z][A-Za-z0-9_.]*$', username) == []:
        raise ValidationError('用户名只能包含字母大小写、数字、点及下划线且以字母开头')
    if User.objects.filter(username=username):
        raise ValidationError('用户名已被使用')

def validators_email(email):
    if User.objects.filter(email=email):
        raise ValidationError('邮箱已注册')

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=16)
    password = forms.CharField(label='密 码', widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=16, validators=[validators_username])
    email = forms.EmailField(label='邮 箱', validators=[validators_email])
    password1 = forms.CharField(label='密 码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)
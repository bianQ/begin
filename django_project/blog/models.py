from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import hashlib
# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    location = models.CharField(max_length=30)

    #生成默认头像
    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.user.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

class Blog(models.Model):
    author = models.ForeignKey(User)
    profile = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=20)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    read = models.IntegerField(default=0)

class Comment(models.Model):
    blog = models.ForeignKey(Blog)
    user = models.ForeignKey(User)
    profile = models.ForeignKey(UserProfile)
    body = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
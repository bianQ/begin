from django.db import models
from django.utils import timezone
# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    email = models.EmailField()
    #member_since = models.DateTimeField()
    #name = models.CharField(max_length=16)
    #location = models.CharField(max_length=20)

class Blog(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField()
    pub_date = models.DateTimeField()
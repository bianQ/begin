from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Blog(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=20)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
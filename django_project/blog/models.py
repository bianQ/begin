from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Blog(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField()
    pub_date = models.DateTimeField()
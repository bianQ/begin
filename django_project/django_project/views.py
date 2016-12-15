from django.shortcuts import redirect
from django.conf import settings


def index(request):
    url = settings.DOMAIN + '/blog'
    return redirect(url)
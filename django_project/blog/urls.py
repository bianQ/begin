from django.conf.urls import url


from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^([0-9]+)/profile/$', views.profile, name='profile'),
    url(r'^active/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.active, name='active')
]
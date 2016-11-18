from django.conf.urls import url


from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/(?P<username>[A-Za-z][A-Za-z0-9_.]*)/$', views.profile, name='profile'),
    url(r'^active/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.active, name='active'),
    url(r'^getpassword/$', views.getpassword, name='getpassword'),
    url(r'^changepassword/$', views.changepassword, name='changepassword'),
    url(r'^newpassword/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.newpassword, name='newpassword'),
    url(r'^article/(?P<id>[0-9]+)/$', views.article, name='article')
]
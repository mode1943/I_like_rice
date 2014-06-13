from django.conf.urls import (patterns, url)
from rice_member import views
urlpatterns = patterns('',
    url(r'^login/$', views.mem_login, name='login'),
    url(r'^reg/$', views.register, name='register'),
    url(r'^logout/$', views.mem_logout, name='logout'),
    )

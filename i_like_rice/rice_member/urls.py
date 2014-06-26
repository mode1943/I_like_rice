from django.conf.urls import (patterns, url)
from rice_member import views
urlpatterns = patterns('',
    url(r'^login/$', views.mem_login, name='login'),
    url(r'^reg/$', views.register, name='register'),
    url(r'^logout/$', views.mem_logout, name='logout'),
    url(r'^applyjoin/$', views.applyfor_group, name='rice_member_applyforgroup'),
    url(r'^accept_group/$', views.accept_group, name='rice_member_acceptgroup'),
    url(r'^creategroup/$', views.create_group, name='rice_member_create_group'),
    )

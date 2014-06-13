from django.conf.urls import (patterns, url)
from rice import views

urlpatterns = patterns('',
    url(r'^demo/$', views.demo, name='demo'),
    url(r'^index/$', views.index, name="index"),
)

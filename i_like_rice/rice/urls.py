from django.conf.urls import (patterns, url)
from rice import views

urlpatterns = patterns('',
    url(r'^index/$', views.index, name='demo'),
)

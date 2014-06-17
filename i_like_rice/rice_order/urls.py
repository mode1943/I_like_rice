from django.conf.urls import (patterns, url)
from rice_order import views

urlpatterns = patterns('',
    url(r'^buy/$', views.buy_rice, name="rice_order_buy_rice"),


)

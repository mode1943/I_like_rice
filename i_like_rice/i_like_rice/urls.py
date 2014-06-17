from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'i_like_rice.views.home', name='home'),
    # url(r'^i_like_rice/', include('i_like_rice.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^member/', include('rice_member.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^rice/', include('rice.urls')),
    url(r'^order/', include('rice_order.urls')),
)

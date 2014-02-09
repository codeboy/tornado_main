# coding: utf-8

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('django_apps.dj_site.urls', namespace='site')),

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'/admin/', include(admin.site.urls)),
)

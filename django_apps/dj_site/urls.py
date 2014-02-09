# coding: utf-8

from django.conf.urls import url, patterns
from django.views.generic.base import TemplateView
from django_apps.dj_site.views import *


urlpatterns = patterns('django_apps.dj_site.views',
    url(r'/hello-django$', 'hello', name='hello'),
)
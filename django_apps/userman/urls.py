# -*- coding: utf-8 -*-
"""urlconf for the consumers application"""

from django.conf.urls import url, patterns, include
from django.views.generic import TemplateView

from views import *


urlpatterns = patterns('boss_tools.userman.views',
    # url(r'^$', 'home', name='home'),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
)


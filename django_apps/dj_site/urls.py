# coding: utf-8

from django.conf.urls import url, patterns
from django.views.generic.base import TemplateView
from django_apps.dj_site import views as base_view


# urlpatterns = patterns('django_apps.dj_site.views',
#     url(r'/hello-django$', 'hello', name='hello'),
# )

urlpatterns = patterns('django_apps.dj_site.views',
    url(r'^hello-django$', base_view.Homepage.as_view(), name='hello'),
    url(r'^register-user$', base_view.RegisterUser.as_view(), name='userinfo'),
)
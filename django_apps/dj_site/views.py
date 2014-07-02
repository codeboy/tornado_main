# coding: utf-8

from django.http import HttpResponse

from django.views.generic import View, TemplateView
from django.views.generic.base import TemplateResponseMixin
from django.core.exceptions import ObjectDoesNotExist

#from django.utils.translation import ugettext_lazy as _
from django_apps.utils import lang_stub as _

from django_apps.mixins import (
    LoginRequiredMixin,
)


class Homepage(
    # LoginRequiredMixin,
    TemplateView,
    View,
):
    """
    homepage
    """
    template_name = 'base.html'


    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        return context


class RegisterUser(
    # LoginRequiredMixin,
    # TemplateView,
    TemplateResponseMixin,
    View,
):
    """
    homepage
    """
    template_name = 'user-info.html'


    def get(self, request, *args, **kwargs):
        print request.user
        context = dict()
        return RegisterUser.render_to_response(self, context)


    # def get_context(self, request):
    #     context = dict()
    #     return context


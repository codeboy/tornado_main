# coding: utf-8

from django.http import HttpResponse

from django.views.generic import View, TemplateView
from django.core.exceptions import ObjectDoesNotExist

#from django.utils.translation import ugettext_lazy as _
from django_apps.utils import lang_stub as _

from django_apps.mixins import (
    LoginRequiredMixin,
)


class Homepage(
    # LoginRequiredMixin,
    # TemplateView,
    View,
):
    """
    homepage
    """
    # template_name = ''

    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello from django")


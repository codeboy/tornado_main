# coding: utf-8

from tornado_apps.BaseHandler import BaseHandler
from django_apps.dj_site.models import TestModel


class HomeHandler(BaseHandler):

    def get(self):
        context = self.context
        context['status'] = "work in progress"

        rTest = TestModel.objects.all()
        context['list'] = rTest

        self.render('index.html', **context)

# coding: utf-8

from tornado_apps.BaseHandler import BaseHandler
from tornado_apps.DjangoHandler import DjangoBaseHandler
from django_apps.dj_site.models import TestModel


class HomeHandler(DjangoBaseHandler):

    def get(self):
        context = dict()
        # context = self.context
        # context['status'] = "work in progress"

        dj_request = self.get_django_request()

        rTest = TestModel.objects.all()
        context['list'] = rTest

        sss = self.render_string('index.html', **context)
        self.write(sss)

        # self.render('index.html', **context)

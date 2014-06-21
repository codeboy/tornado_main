# coding: utf-8

from tornado_apps.BaseHandler import BaseHandler
from tornado_apps.BaseDjangoHandler import DjangoBaseHandler
from django_apps.dj_site.models import TestModel


class MainPage(DjangoBaseHandler):

    def get(self):
        context = dict()
        # context = self.context
        # context['status'] = "work in progress"

        dj_request = self.get_django_request()

        t = self.render_string('pages/main.html', **context)
        self.write(t)


class BlankPage(DjangoBaseHandler):

    def get(self):
        context = dict()
        # context = self.context
        # context['status'] = "work in progress"

        dj_request = self.get_django_request()

        rTest = TestModel.objects.all()
        context['list'] = rTest

        t = self.render_string('pages/blank.html', **context)
        self.write(t)


class BlankWidgetPage(DjangoBaseHandler):

    def get(self):
        context = dict()
        # context = self.context
        # context['status'] = "work in progress"

        dj_request = self.get_django_request()

        rTest = TestModel.objects.all()
        context['list'] = rTest

        t = self.render_string('pages/blank_widget.html', **context)
        self.write(t)



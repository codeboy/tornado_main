# coding: utf-8

from tornado_apps.BaseHandler import BaseHandler
from tornado_apps.BaseDjangoHandler import DjangoBaseHandler
from django_apps.dj_site.models import TestModel


class HomeHandler(DjangoBaseHandler):

    def get(self):
        context = dict()
        # context = self.context
        # context['status'] = "work in progress"

        d_request = self.get_django_request()

        user_name = d_request.user.username
        context['user_name'] = user_name

        t = self.render_string('index_sadmin.html', **context)
        self.write(t)

        # self.render('index.html', **context)

# -*- coding: utf-8 -*-
from tornado_apps.BaseHandler import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        context = self.context
        context['status'] = "work in progress"

        self.render('index.html', **context)

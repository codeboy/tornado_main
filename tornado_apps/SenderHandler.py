# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import datetime
from tornado.escape import json_decode

from django.utils.http import urlencode

from tornado_apps.BaseHandler import BaseHandler
import tornado_settings_local as TSL

class SenderHandler(BaseHandler):

    def get(self):
        context = self.context
        self.render('sender.html', **context)


    def post(self, *args, **kwargs):
        context = self.context
        context['status'] = "work in progress"

        number = self._get_safe_argument('number')
        message = self._get_safe_argument('message')

        if not number: context['status'] = "enter number"
        if not message: context['status'] = "enter message"

        url = 'http://gate.smsaero.ru/send/'
        url2 = 'http://gate.smsaero.ru/balance/'

        m = hashlib.md5()
        m.update(TSL.PASSWORD)
        password = m.hexdigest()

        params_dict = dict({
            'to':number,
            'text': message,
            'user' : TSL.USER,
            'password' : password,
            'from' : 'codeboy',
            'date' : time.time()
        })
        params_dict2 = dict({
            'user' : TSL.USER,
            'password' : password,
        })
        params = urlencode(params_dict)
        print params
        r = requests.post(url, data=params_dict)
        print dir(r)
        print r.status_code
        print r.text
        print r.links

        context['status'] = 'code: %s | status: %s' % (r.status_code, r.text)

        self.render('sender.html', **context)
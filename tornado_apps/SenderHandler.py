# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import datetime
from tornado.escape import json_decode

from django.utils.http import urlencode

from tornado_apps.BaseHandler import BaseHandler
import tornado_settings.t_settings_local as TSL


class SenderHandler(BaseHandler):
    """
    отправка смс
    """

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

        m = hashlib.md5()
        m.update(TSL.PASSWORD)
        password = m.hexdigest()

        params_dict = dict({
            'to':number,
            'text': message,
            'user' : TSL.USER,
            'password' : password,
            'from' : 'codeboy.ru',
            # 'date' : time.time()
        })
        params = urlencode(params_dict)
        r = requests.post(url, data=params_dict)

        context['status'] = 'code: %s | status: %s' % (r.status_code, r.text)

        self.render('sender.html', **context)



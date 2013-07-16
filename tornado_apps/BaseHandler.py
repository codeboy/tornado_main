# -*- coding: utf-8 -*-

import tornado.web
from exeption_util import MyDefaultException


class BaseHandler(tornado.web.RequestHandler):
    """
    base class for others handlers

    базовый класс для остальных хендлеров
    """

    context = dict()

    def initialize(self):
        self.context = ''
        self.context = dict()


    def get(self):
        """
        if in inherit class not define GET show 404

        если в дочернем классе не определён метод get покажем 404 страницу
        """
        self.set_status(404)
        self.write('{"status":"error","msg":"Page not found"}')


    def _get_safe_argument(self, name):
        """
        т.к. работа с POST данными в торнадо не удобная приходится немого повозиться
        родной get_argument сразу возвращает 404, а это не удобно,
        приходится брать get_arguments который возвращяет словарь.
        если нам вернули несоклько переменных, то мы отдаём последнюю
        """
        arg = self.get_arguments(name)
        if len(arg) >= 1:
            return arg[-1]
        else:
            return False


    # def get_error_html(self, status_code, **kwargs):
        # self.write(self.render_string("404.html"))


    def set_json_type(self):
        self.set_header("Content-Type", "application/json")



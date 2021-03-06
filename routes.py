# coding: utf-8

import tornado.web
from tornado_apps import (
    BaseHandler,
    HomeHandler,
    SenderHandler,
    AjaxPage
)

import tornado_settings.t_settings as TS


# there is routes for all parts of project
ROUTES = [
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": TS.STATIC_PATH}),

    (r'/', HomeHandler.HomeHandler),

    (r'/send-sms', SenderHandler.SenderHandler),

    (r'/page/dashboard', AjaxPage.Dashboard),
    (r'/page/blank', AjaxPage.BlankPage),

]
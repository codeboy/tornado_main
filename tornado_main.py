# -*- coding: utf-8 -*-

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

import tornado_settings as TS
define('port', type=int, default=8080)
# define('port', type=int, default=TS.PORT)

from tornado_apps import (
    BaseHandler,
    HomeHandler,
    SenderHandler,
)


def main():
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        [
            (r'/', HomeHandler.HomeHandler),
            (r'/send-sms/', SenderHandler.SenderHandler),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ], template_path=TS.TEMPLATE_PATH, debug = TS.DEBUG)
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
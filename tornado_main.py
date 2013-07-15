# -*- coding: utf-8 -*-

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

# define('port', type=int, default=8080)
define('port', type=int, default=80)

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")


class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado')


def main():
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        [
            (r'/', BaseHandler),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
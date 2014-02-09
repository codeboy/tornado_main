# coding: utf-8

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings.settings")

import tornado_settings.t_settings as TS
define('port', type=int, default=8000)
# define('port', type=int, default=TS.PORT)

from tornado_apps import (
    BaseHandler,
    HomeHandler,
    SenderHandler,
)


def main():
    tornado.options.define('debug', default=False)

    wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())

    handlers = [
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": TS.STATIC_PATH}),

        (r'/', HomeHandler.HomeHandler),

        (r'/send-sms/', SenderHandler.SenderHandler),
        ('/dj/.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
    ]

    settings = {
        'template_path' : TS.TEMPLATE_PATH,
        'debug' : TS.DEBUG,
        'static_path': TS.STATIC_PATH,
        'st': TS.STATIC_PATH,
    }

    tornado_app = tornado.web.Application(handlers, **settings)

    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()



aaa = '''
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/users", UsersHandler),
        ]
        settings = dict(
            cookie_secret="some_long_secret_and_other_settins"
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        # Have one global connection.
        self.db = scoped_session(sessionmaker(bind=engine))
'''
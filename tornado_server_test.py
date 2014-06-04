# tornado_django_wrapper.py Raw

############# init parent django project settings
from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import settings

from django.core.management import setup_environ
setup_environ(settings)
###############


import django.conf as dj_conf
import django.contrib.auth as dj_auth
import django.core.handlers.wsgi as dj_wsgi
import django.db as dj_db
import django.utils.importlib as dj_importlib
import logging
import tornado.options
import tornado.web as t_web

class BaseHandler(t_web.RequestHandler):
  def prepare(self):
    super(BaseHandler, self).prepare()
    # Prepare ORM connections
    dj_db.connection.queries = []

  def finish(self, chunk = None):
    super(BaseHandler, self).finish(chunk = chunk)
    # Clean up django ORM connections
    dj_db.connection.close()
    logging.info('%d sql queries' % len(dj_db.connection.queries))
    for query in dj_db.connection.queries:
      logging.debug('%s [%s seconds]' % (query['sql'], query['time']))

    # Clean up after python-memcached
    from django.core.cache import cache
    if hasattr(cache, 'close'):
      cache.close()

  def get_django_session(self):
    if not hasattr(self, '_session'):
      engine = dj_importlib.import_module(
        dj_conf.settings.SESSION_ENGINE)
      session_key = self.get_cookie(dj_conf.settings.SESSION_COOKIE_NAME)
      self._session = engine.SessionStore(session_key)
    return self._session

  def get_user_locale(self):
    # locale.get will use the first non-empty argument that matches a
    # supported language.
    return tornado.locale.get(
      self.get_argument('lang', None),
      self.get_django_session().get('django_language', None),
      self.get_cookie('django_language', None))

  def get_current_user(self):
    # get_user needs a django request object, but only looks at the session
    class Dummy(object): pass
    django_request = Dummy()
    django_request.session = self.get_django_session()
    user = dj_auth.get_user(django_request)
    if user.is_authenticated():
      return user
    else:
      # try basic auth
      if not self.request.headers.has_key('Authorization'):
        return None
      kind, data = self.request.headers['Authorization'].split(' ')
      if kind != 'Basic':
        return None
      (username, _, password) = data.decode('base64').partition(':')
      user = dj_auth.authenticate(username = username,
                                              password = password)
      if user is not None and user.is_authenticated():
        return user
      return None

  def get_django_request(self):
    request = dj_wsgi.WSGIRequest(
      tornado.wsgi.WSGIContainer.environ(self.request))
    request.session = self.get_django_session()

    if self.current_user:
      request.user = self.current_user
    else:
      request.user = dj_auth.models.AnonymousUser()

    return request


#-------------------------------------------------------

from tornado_django_wrapper import BaseHandler
import tornado.web
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/pull/", PullHandler),
            (r"/push/", PushHandler),
        ]
        tornado.web.Application.__init__(self, handlers)

class DataMixin(object):
    waiters = set()

    def wait_for_messages(self, callback):
        cls = MessageMixin
        cls.waiters.add(callback)

    def cancel_wait(self, callback):
        cls = MessageMixin
        cls.waiters.remove(callback)

    def new_messages(self, messages):
        cls = MessageMixin
        future = set()
        for callback in cls.waiters:
            try:
                callback(messages)
            except:
                logging.error("Error in waiter callback", exc_info=True)


class PushHandler(BaseHandler, DataMixin):
    def post(self):
        message = self.get_argument("message")
        self.new_messages([message])
        self.finish({'m': message})


class PullHandler(BaseHandler, DataMixin):
    @tornado.web.asynchronous
    def post(self):
        self.django_info = self.get_django_session().get("anything", None)
        self.wait_for_messages(self.on_new_messages)

    def on_new_messages(self, messages):
        # Closed client connection
        if self.request.connection.stream.closed():
            return
        self.finish(dict(messages=messages))

    def on_connection_close(self):
        self.cancel_wait(self.on_new_messages)


if __name__ == "__main__":
    app = Application()
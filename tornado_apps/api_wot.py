from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web

class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = { 'version': '3.5.1',
                     'last_build':  date.today().isoformat() }
        self.write(response)

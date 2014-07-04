# coding: utf-8

from tornado_apps.BaseHandler import BaseHandler
from tornado_apps.BaseDjangoHandler import DjangoBaseHandler
from django_apps.dj_site.models import TestModel

from tornadobabel.mixin import TornadoBabelMixin
# from tornadobabel.locale import load_gettext_translations
from tornadobabel import locale

from django_apps.userman.models import UserProfile
from django_apps.gamesapp.models import Game
from django_apps.teamapp.models import Team
from django_apps.userman.models import UserProfile
from django.contrib.auth.models import User

from django_apps.gamesapp.games_accounts import Wot

import requests

class Dashboard(DjangoBaseHandler):

    def get(self):
        context = dict()
        # context = self.context
        # context['status'] = "work in progress"

        q_games = Game.objects.all()
        context['games'] = q_games
        q_teams = Team.objects.all()
        context['teams'] = q_teams
        q_users = UserProfile.objects.select_related().all()
        context['users'] = q_users

        url = 'http://api.worldoftanks.ru/wot/account/list/?'
        app_id = 'application_id=%s' % Wot.app_id
        user = '&search=codeboy'
        r = requests.get('{0}{1}{2}'.format(
            url, app_id,user
        ))
        result = r.json()
        print result['data'][0]['account_id']

        t = self.render_string('pages/main.html', **context)
        # self.set_header("Content-Type", "text/javascript; charset=UTF-8")
        # self.set_header("Content-Type", "application/json")

        return self.write(t)


class BlankPage(DjangoBaseHandler):

    def get(self):
        context = dict()
        # context = self.context
        # context['status'] = "work in progress"

        dj_request = self.get_django_request()

        rTest = TestModel.objects.all()
        context['list'] = rTest

        t = self.render_string('pages/blank.html', **context)
        self.write(t)





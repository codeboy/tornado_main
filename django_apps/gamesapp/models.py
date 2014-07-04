# coding: utf-8

import datetime
from random import randrange

from django.db import models as m
from django.template.defaultfilters import slugify

# from django.utils.translation import ugettext_lazy as _
from django_apps.utils import lang_stub as _
# from django_apps import models_list as ml
from django.contrib.auth.models import User
from django_apps.teamapp.models import Team


class Game(m.Model):
    """
    team model
    """
    name = m.CharField(max_length=245, verbose_name=_('name'))
    name_slug = m.SlugField(max_length=250, verbose_name=_('slug name'),)
    logo = m.CharField(max_length=150, blank=True, null=True)
    description = m.TextField(blank=True, null=True)

    link_game = m.URLField(blank=True, null=True)
    link_user_profile = m.CharField(max_length=250, blank=True, null=True)
    link_team_profile = m.CharField(max_length=250, blank=True, null=True)

    datetime_created = m.DateTimeField(editable=False, default=datetime.datetime.now, verbose_name=_('creation date'),)
    datetime_modified = m.DateTimeField(editable=False, default=datetime.datetime.now, verbose_name=_('modified date'),)

    # class Meta:
    #     verbose_name, verbose_name_plural = _(u'Comment'), _(u'Comments')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name_slug is None:
            self.name_slug = slugify(self.name)
        self.datetime_modified = datetime.datetime.now()
        super(Game, self).save(*args, **kwargs)


class TeamGame(m.Model):
    game = m.ForeignKey(Game)
    team = m.ForeignKey(Team)

    ingame_name = m.CharField(max_length=120, blank=True, null=True)
    ingame_logo = m.CharField(max_length=250, blank=True, null=True)
    description = m.TextField(blank=True, null=True)

    datetime_created = m.DateTimeField(editable=False, default=datetime.datetime.now, verbose_name=_('creation date'),)
    datetime_modified = m.DateTimeField(editable=False, default=datetime.datetime.now, verbose_name=_('modified date'),)

    def save(self, *args, **kwargs):
        self.datetime_modified = datetime.datetime.now()
        super(TeamGame, self).save(*args, **kwargs)


class UserGame(m.Model):
    game = m.ForeignKey(Game)
    user = m.ForeignKey(User)

    nickname_name = m.CharField(max_length=120, blank=True, null=True)

    datetime_created = m.DateTimeField(editable=False, default=datetime.datetime.now, verbose_name=_('creation date'),)
    datetime_modified = m.DateTimeField(editable=False, default=datetime.datetime.now, verbose_name=_('modified date'),)

    def save(self, *args, **kwargs):
        self.datetime_modified = datetime.datetime.now()
        super(UserGame, self).save(*args, **kwargs)
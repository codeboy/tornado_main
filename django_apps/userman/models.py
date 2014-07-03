# coding: utf-8

import datetime
from random import randrange

from django.db import models as m
from django.contrib.auth.models import (
    User,
    Permission,
    Group,
)

# from django.utils.translation import ugettext_lazy as _
from django_apps.utils import lang_stub as _


class MainUser(User):
    date_of_birth = m.DateField(blank=True, null=True,)
    activated = m.BooleanField(default=False)
    activation_key = m.PositiveIntegerField(max_length=16, blank=True, null=True)
    avatar = m.CharField(max_length=150)

    datetime_created = m.DateTimeField(editable=False, default=datetime.datetime.now, verbose_name=_('creation date'),)
    datetime_modified = m.DateTimeField(editable=False, default=datetime.datetime.now, verbose_name=_('modified date'),)

    def __unicode__(self):
        return '%s - %s - %s' % (self.id, self.get_item_type_display(), self.state)

    def save(self, *args, **kwargs):
        self.datetime_modified = datetime.datetime.now()
        super(MainUser, self).save(*args, **kwargs)
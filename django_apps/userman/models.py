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


# from django.contrib.auth.models import UserManager
class UserProfile(m.Model):
    # objects = UserManager()
    user = m.OneToOneField(User)

    date_of_birth = m.DateField(blank=True, null=True,)
    activated = m.BooleanField(default=False)
    activation_key = m.PositiveIntegerField(max_length=16, blank=True, null=True)
    avatar = m.CharField(max_length=150, blank=True, null=True,)

    datetime_created = m.DateTimeField(editable=False, default=datetime.datetime.now, verbose_name=_('creation date'),)
    datetime_modified = m.DateTimeField(editable=False, default=datetime.datetime.now, verbose_name=_('modified date'),)

    def __unicode__(self):
        return '%s' % self.user

    def save(self, *args, **kwargs):
        self.datetime_modified = datetime.datetime.now()
        super(UserProfile, self).save(*args, **kwargs)
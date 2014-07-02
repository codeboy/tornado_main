#-*- coding: utf-8 -*-

import datetime
from random import randrange

from django.db import models as m
from django.contrib.auth.models import (
    User,
    Permission,
    Group,
)

#from django.utils.translation import ugettext_lazy as _
from boss_tools.site.utils import lang_stub as _


# this is GROUPS
class GroupAsRole(m.Model):
    u"""
    ЭТО НЕ РОЛИ!!!
    это на самом деле ГРУППЫ в понимании проектировщиков =)
    """
    PROJECT_CHOICES = ((1, 'hosting'),)
    name = m.CharField(max_length=120)
    project = m.PositiveIntegerField(choices=PROJECT_CHOICES, default=1)

    # поле отношений с группами, но для проекта это отношение с РОЛЯМИ
#    roles = m.ManyToManyField(Group, blank=True, null=True,)
    roles2 = m.ManyToManyField(Group, blank=True, null=True,)

    def __unicode__(self):
        return u'%s' % self.name

    def get_roles(self):
        return ", ".join([s.name for s in self.roles2.all()])


class MainUser(User):
    date_of_birth = m.DateField(blank=True, null=True,)
    group_as_roles = m.ManyToManyField(GroupAsRole, blank=True, null=True, verbose_name=_('таки группы, да!'))
#    is_social = m.BooleanField(default=False, verbose_name=_('is from social auth'))


CONTACT_TYPE_CHOICES = (
    (1, 'skype'),
    (2, 'jabber'),
    (3, 'icq'),
    (4, 'phone'),
    (5, 'email')
)
class UserContact(m.Model):
    """
    модель для хранения контактов пользователя - жабер, скайп, и т.д.
    """
    CONTACT_TYPE_CHOICES = CONTACT_TYPE_CHOICES

    user = m.ForeignKey(MainUser)
    contact_type = m.PositiveIntegerField(choices=CONTACT_TYPE_CHOICES, max_length=2)
    contact = m.CharField(max_length=250)
    is_main = m.BooleanField(default=False)
    activated = m.BooleanField(default=False)
    activation_key = m.PositiveIntegerField(max_length=16, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s - %s' % (self.user, self.contact_type, self.contact)

    def save(self, *args, **kwargs):
        if not self.activated and not self.activation_key:
            self.activation_key = randrange(pow(10, 8), (pow(10, 9)-1))
        super(UserContact, self).save(*args, **kwargs)


class PasswordRecovery(m.Model):
    user = m.ForeignKey(MainUser)
    created_at = m.DateTimeField(auto_now_add=True)
    modified_at = m.DateTimeField(auto_now=True)
    activated = m.BooleanField(default=False)
    activation_key = m.PositiveIntegerField(
        max_length=16, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if not self.activated and not self.activation_key:
            self.activation_key = randrange(pow(10, 8), (pow(10, 9)-1))
        super(PasswordRecovery, self).save(*args, **kwargs)

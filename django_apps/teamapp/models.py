# coding: utf-8

import datetime

from django.db import models as m
from django.template.defaultfilters import slugify

# from django.utils.translation import ugettext_lazy as _
from django_apps.utils import lang_stub as _
# from django_apps import models_list as ml

from django.contrib.auth.models import User


class Team(m.Model):
    """
    team model
    """
    name = m.CharField(max_length=245, verbose_name=_('name'))
    name_slug = m.SlugField(max_length=250, verbose_name=_('slug name'),)
    logo = m.CharField(max_length=150, blank=True, null=True)
    description = m.TextField(blank=True, null=True)
    owner = m.ForeignKey(User)

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
        super(Team, self).save(*args, **kwargs)


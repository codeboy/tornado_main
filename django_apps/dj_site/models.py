# coding: utf-8

from django.db import models as m


class TestModel(m.Model):

    name = m.CharField(max_length=200)
    description = m.TextField()
    born = m.DateField(blank=True, auto_now=True)
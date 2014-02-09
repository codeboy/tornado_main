# coding: utf-8

from django.contrib import admin
from django_apps.dj_site.models import TestModel


class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(TestModel, AuthorAdmin)
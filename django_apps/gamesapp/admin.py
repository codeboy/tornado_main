# -*- coding: utf-8 -*-

from django.contrib import admin
from thirdparty.treebeard.admin import TreeAdmin

from models import Game, TeamGame, UserGame


class DefaultAdmin(admin.ModelAdmin):
    save_on_top = True

class MixedSlugAdmin(DefaultAdmin):
    prepopulated_fields = {"name_slug": ("name",)}

admin.site.register(Game, MixedSlugAdmin)

admin.site.register(TeamGame, DefaultAdmin)
admin.site.register(UserGame, DefaultAdmin)

# admin.site.register(Country, TreeAdmin)

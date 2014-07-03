# -*- coding: utf-8 -*-

from django.contrib import admin
from thirdparty.treebeard.admin import TreeAdmin

from models import Team


class DefaultAdmin(admin.ModelAdmin):
    save_on_top = True

class MixedSlugAdmin(DefaultAdmin):
    prepopulated_fields = {"name_slug": ("name",)}

admin.site.register(Team, MixedSlugAdmin)

# admin.site.register(ProviderUrl, DefaultAdmin)
# admin.site.register(Country, TreeAdmin)

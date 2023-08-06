from django.contrib import admin
from . import models
from django_tree_materialized.admin import MPAdmin


class TreeAdmin1(MPAdmin):
    pass


admin.site.register(models.Tree, TreeAdmin1)

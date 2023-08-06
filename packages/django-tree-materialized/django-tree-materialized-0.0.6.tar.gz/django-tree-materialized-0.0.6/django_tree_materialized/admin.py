from django.contrib import admin
from . import models


class MPAdmin(admin.ModelAdmin):
    readonly_fields = ('level', 'path')
    list_display = ('id', 'parent', 'level', 'path')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        obj.level = 1

        if obj.parent:
            obj.level = obj.parent.level + 1
            obj.path = obj.parent.path + models.MPTree.number_to_str(obj.id)
        else:
            obj.path = models.MPTree.number_to_str(obj.id)

        obj.save()

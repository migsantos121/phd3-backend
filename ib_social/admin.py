from django.contrib import admin

from . import models


class MemberRelationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'm_id',
        'm_type',
        'r_m_id',
        'r_m_type',
        'relation',
        'status',
        'is_deleted',
        'source'
    )

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(models.MemberRelation, MemberRelationAdmin)
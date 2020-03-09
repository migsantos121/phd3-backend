from django.contrib import admin
from ib_notifications import models


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'source',
        'cm_type',
        'title',
        'message'
    )

    list_filter = (
        'source',
        'cm_type',
        'title',
    )

    search_fields = (
        'source',
        'cm_type',
        'title',
        'message'
    )


class NotificationReceiverAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_id',
        'read_status',
        'read_at'
    )

    search_fields = (
        'user_id',
        'read_status'
    )


class NotificationChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'source',
        'name',
        'display_name'
    )


class UserCMTokenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_id',
        'cm_type',
        'cm_token',
        'source'
    )

    search_fields = (
        'user_id',
        'cm_type'
        'cm_token'
    )


class UserNotificationChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_id',
        'notification_choice_id',
        'preference'
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Notification, NotificationAdmin)
_register(models.NotificationReceiver, NotificationReceiverAdmin)
_register(models.UserCMToken, UserCMTokenAdmin)
_register(models.NotificationChoice, NotificationChoiceAdmin)
_register(models.UserNotificationChoice, UserNotificationChoiceAdmin)

def get_user_notification_choices_response(request_data, user):
    source = request_data["source"]
    from ib_notifications.models.user_notification_choices import UserNotificationChoice
    response_object = UserNotificationChoice.get_user_notification_choices_source(source=source, user=user)
    return response_object
def update_user_notification_choice_response(request_data, user):
    source = request_data['source']
    name = request_data.get('display_name', None)
    preference = request_data['preference']
    from ib_notifications.models.user_notification_choices import UserNotificationChoice
    response_object = UserNotificationChoice.update_user_notification_preference(user=user, source=source,
                                                                                 name=name, preference=preference)
    return response_object
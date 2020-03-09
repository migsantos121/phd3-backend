def add_notification_choice_response(request_data):
    source = request_data['source']
    name = request_data['name']
    display_name = request_data.get('display_name', None)
    default_choice = request_data.get('default_choice', 'ON')
    from ib_notifications.models.notification_choices import NotificationChoice
    response_object = NotificationChoice.add_notification_choice(source=source, name=name,
                                                                 display_name=display_name,
                                                                 default_choice=default_choice)
    return response_object

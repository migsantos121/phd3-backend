def add_or_update_user_cm_token(request_data, user):
    from ib_notifications.constants.device_types import DeviceType

    cm_type = request_data['cm_type']
    cm_token = request_data['cm_token']
    source = request_data['source']
    device_id = request_data.get('device_id', '')
    device_type = request_data.get('device_type', DeviceType.DEFAULT.value)

    if cm_token == "" or cm_token is None:
        from ib_notifications.utilities.exceptions.cm_token_is_null import CMTokenIsNull
        raise CMTokenIsNull('CMToken can not be null')
    from ib_notifications.models import UserCMToken
    response_object = UserCMToken.update_user_cm_tokens(user=user, cm_type=cm_type, cm_token=cm_token, source=source,
                                                        device_id=device_id, device_type=device_type)
    return response_object

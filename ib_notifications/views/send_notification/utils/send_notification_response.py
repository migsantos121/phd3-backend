import json

from django.conf import settings
from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed

from ib_notifications.constants.device_types import DEVICE_TYPES


def send_notification_response(request_data, user):
    from ib_notifications.constants.push_notification_types import PushNotificationTypes

    name = request_data['name']
    title = request_data["title"]
    source = request_data["source"]
    message = request_data["message"]
    cm_type = request_data['cm_type']
    user_id_list = request_data.get('user_ids', [])
    extra_data = request_data.get("extra_data", '')
    notification_type = request_data.get("notification_type", "")
    log_notification = request_data.get("log_notification", True)
    device_types = request_data.get('device_types', [])
    push_notification_type = request_data.get('push_notification_type', PushNotificationTypes.DATA.value)

    for device_type in device_types:
        if device_type not in DEVICE_TYPES:
            from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
            raise BadRequest('Invalid device type')

    try:
        json.loads(request_data.get("extra_data", {}))
    except:
        raise ExpectationFailed({}, "extra_data is not in the json.dumps format. Unable to process")

    from ib_notifications.models.user_cm_tokens import UserCMToken
    response_object = UserCMToken.send_notification(source=source, name=name, title=title, extra_data=extra_data,
                                                    cm_type=cm_type, log_notification=log_notification, user=user,
                                                    message=message, user_id_list=user_id_list,
                                                    notification_type=notification_type,
                                                    device_types=device_types,
                                                    push_notification_type=push_notification_type)

    return response_object

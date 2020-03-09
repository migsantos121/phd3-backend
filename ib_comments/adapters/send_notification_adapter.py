from requests import HTTPError


def send_notification_adapter(user, access_token, source, name, title, message, extra_data, user_ids, cm_type,
                              notification_type, log_notification):
    from django.conf import settings
    request_type = settings.IB_NOTIFICATIONS_REQUEST_TYPE
    from ib_notifications.interfaces.CommonInterface import CommonInterface
    common_interface_object = CommonInterface(user=user, access_token=access_token, request_type=request_type)
    try:
        send_notification_response = common_interface_object.send_notification_interface(source=source, name=name,
                                                                                         title=title, message=message,
                                                                                         extra_data=extra_data,
                                                                                         user_ids=user_ids,
                                                                                         cm_type=cm_type,
                                                                                         notification_type=notification_type,
                                                                                         log_notification=log_notification, )
        return send_notification_response
    except HTTPError, err:
        from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
        raise ExpectationFailed({}, res_status="ib_notifications send notification exception: " + err.response.content)

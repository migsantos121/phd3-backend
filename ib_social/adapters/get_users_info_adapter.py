from requests import HTTPError


def get_users_info_adapter(user, access_token, user_ids):
    from ib_users.interfaces.CommonInterface import CommonInterface
    from django.conf import settings
    request_type = settings.IB_USERS_REQUEST_TYPE
    common_interface_object = CommonInterface(user=user, access_token=access_token, request_type=request_type)
    try:
        ib_users_response = common_interface_object.get_minimal_details_by_user_ids(user_ids)
        return ib_users_response
    except HTTPError, err:
        from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
        raise ExpectationFailed({}, res_status="ib_users get_user_details_error error : "+err.response.content)

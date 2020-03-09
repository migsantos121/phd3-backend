from requests import HTTPError


def get_friends_list_adapter(user_id, user_type, limit, offset, user, access_token):
    from ib_social.interfaces.CommonInterface import CommonInterface
    from django.conf import settings
    request_type = settings.IB_SOCIAL_REQUEST_TYPE
    common_interface_object = CommonInterface(user=user, access_token=access_token, request_type=request_type)
    try:
        friends_list = common_interface_object.get_friends_list(m_id=user_id, m_type=user_type, limit=limit, offset=offset,
                                                                search_q="")
        return friends_list
    except HTTPError, err:
        from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
        raise ExpectationFailed({}, res_status="ib_social get_friends_list_adapter error : " + err.response.content)

    # return [
    #     {
    #         "user_id": 1,
    #         "user_name": "vara",
    #         "user_thumbnail": "thumbnail"
    #     },
    #     {
    #         "user_id": 2,
    #         "user_name": "vara",
    #         "user_thumbnail": "thumbnail"
    #     },
    #     {
    #         "user_id": 3,
    #         "user_name": "vara",
    #         "user_thumbnail": "thumbnail"
    #     }
    # ]

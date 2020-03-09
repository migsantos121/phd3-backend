from requests import HTTPError


def get_names_from_userids_adapter(user, access_token, user_ids):
    from ib_users.interfaces.CommonInterface import CommonInterface
    from django.conf import settings
    request_type = settings.IB_USERS_REQUEST_TYPE
    common_interface_object = CommonInterface(user=user, access_token=access_token, request_type=request_type)
    try:
        ib_users_response = common_interface_object.get_minimal_details_by_user_ids(user_ids)
        user_name_objects = []

        for ib_user in ib_users_response:
            user_name_objects.append({
                'user_id': ib_user.get('m_id', None),
                'name': ib_user.get('m_name', None)
            })
        return user_name_objects
    except HTTPError, err:
        from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
        raise ExpectationFailed({}, res_status="ib_connect service error : " + err.response.content)

        # return [
        #     {
        #         "user_id": 1,
        #         "name": "vara",
        #         "res_status": "string"
        #     },
        #     {
        #         "user_id": 2,
        #         "name": "kumar",
        #         "res_status": "string"
        #     }
        # ]

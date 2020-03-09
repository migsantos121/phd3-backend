from requests import HTTPError


def get_stake_holder_adapter(user, access_token, member_id, member_type):
    from ib_connect.interfaces.CommonInterface import CommonInterface
    from django.conf import settings
    request_type = settings.IB_CONNECT_REQUEST_TYPE
    common_interface_object = CommonInterface(user=user, access_token=access_token, request_type=request_type)
    try:
        stake_holder_response = common_interface_object.get_stack_holder(sh_id=member_id, sh_type=member_type)
        print "STAKE HOLDER RESPONSE : ", stake_holder_response, type(stake_holder_response)
        return stake_holder_response
    except HTTPError,err:
        from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
        raise ExpectationFailed({}, res_status="ib_connect service error : "+err.response.content)

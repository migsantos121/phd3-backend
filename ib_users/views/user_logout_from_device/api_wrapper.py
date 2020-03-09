from .validator_class import ValidatorClass
from django_swagger_utils.drf_server.utils.decorator.interface_decorator import validate_decorator


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args,**kwargs):
    request_data = kwargs['request_data']
    user = kwargs['user']
    access_token = kwargs['access_token']
    source = kwargs['source']

    device_id = request_data.get('device_id', '')
    device_type = request_data.get('device_type', '')

    device_info = {'device_id': device_id, 'device_type': device_type}

    from ib_users.models import IBUser
    response_object = IBUser.user_logout(user, access_token, device_info=device_info, source=source)
    from django_swagger_utils.drf_server.utils.server_gen.endpoint_response import endpoint_response
    response_tuple = endpoint_response(response_object)

    return response_tuple

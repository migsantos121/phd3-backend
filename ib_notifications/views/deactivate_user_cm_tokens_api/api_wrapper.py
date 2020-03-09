from .validator_class import ValidatorClass
from django_swagger_utils.drf_server.utils.decorator.interface_decorator import validate_decorator


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    request_data = kwargs.get('request_data', None)

    if not request_data:
        from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
        raise BadRequest('Invalid request data')

    source = request_data.get('source', '')
    user_id = request_data.get('user_id', '')
    device_types = request_data.get('device_types', None)

    device_id = request_data.get('device_id', '')
    cm_token = request_data.get('cm_token', '')

    from ib_notifications.models import UserCMToken
    UserCMToken.deactivate_tokens(cm_token=cm_token, device_id=device_id, source=source, user_id=user_id,
                                  device_types=device_types)
    return

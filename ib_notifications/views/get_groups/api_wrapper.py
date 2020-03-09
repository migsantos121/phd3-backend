from django_swagger_utils.drf_server.utils.decorator.interface_decorator import validate_decorator

from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs['user']
    access_token = kwargs['access_token']
    request_data = kwargs['request_data']

    offset = request_data.get('offset', None)
    limit = request_data.get('limit', None)
    source = request_data.get('source', None)
    group_type = request_data.get('group_type', None)
    from ib_notifications.models import NotificationGroup
    response = NotificationGroup.get_groups(offset, limit, source, group_type, user, access_token)
    return response

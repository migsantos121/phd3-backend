
from .validator_class import ValidatorClass
from django_swagger_utils.drf_server.utils.decorator.interface_decorator import validate_decorator


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs['user']
    request_data = kwargs['request_data']

    limit = request_data["limit"]
    offset = request_data["offset"]
    source = request_data["source"]
    sort_by_date = request_data['sort_by_date']

    from ib_notifications.models import Notification
    response_object = Notification.get_user_notifications_object(source, offset, limit, user, sort_by_date)

    return response_object

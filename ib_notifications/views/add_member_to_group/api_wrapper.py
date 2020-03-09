from django_swagger_utils.drf_server.utils.decorator.interface_decorator import validate_decorator

from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user = kwargs['user']
    access_token = kwargs['access_token']
    request_data = kwargs['request_data']

    entity_id = request_data.get('entity_id', None)
    entity_type = request_data.get('entity_type', None)
    group_name = request_data.get('group_name', None)
    group_type = request_data.get('group_type', 'GENERAL')
    user_ids = request_data.get('user_ids', None)
    source = request_data['source']

    from ib_notifications.models import NotificationGroupMember
    response = NotificationGroupMember.add_notification_group_member(user_ids=user_ids, entity_id=entity_id,
                                                                     entity_type=entity_type,
                                                                     group_name=group_name,
                                                                     group_type=group_type, source=source,
                                                                     user=user,
                                                                     access_token=access_token)
    return response

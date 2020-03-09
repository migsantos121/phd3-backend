
def get_actions_summary_response(request_object, user):

    source = request_object["source"]
    entity_id = request_object["entity_id"]
    entity_type = request_object["entity_type"]
    action_types = request_object["action_types"]

    from ib_action.models import Action
    response_object = Action.get_actions_summary(source=source, entity_type=entity_type, entity_id=entity_id, user_id=user.id, action_type_filters=action_types)
    return response_object
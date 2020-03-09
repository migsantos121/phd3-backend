from ib_action.models import Action


def add_action_response(request_object, user, source, access_token):

    action_value = request_object["action_value"]
    req_source = request_object["source"]
    entity_id = request_object["entity_id"]
    action_type = request_object["action_type"]
    entity_type = request_object["entity_type"]

    response_object, callback_dict = Action.add_action_record(action_value=action_value, source=req_source,
                                                              entity_id=entity_id, action_type=action_type,
                                                              entity_type=entity_type, user_id=user.id)
    from ib_action.views.add_action.callback_handler import callback_handler
    callback_handler(source, 'ib_action', 'add_action', access_token, 1, callback_dict)
    return response_object

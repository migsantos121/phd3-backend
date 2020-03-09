
def get_users_actions_summary_response(request_object, user):

    source = request_object["source"]
    entities = request_object["entities"]
    action_types = request_object["action_types"]
    user_ids = request_object["user_ids"]

    from ib_action.models import Action
    response_object = Action.get_selected_users_actions_summary(source=source, entities=entities, user_ids=user_ids, action_type_filters=action_types)
    return response_object
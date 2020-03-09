def get_user_action_entities_response(request_data, user):
    request_data["user_id"] = user.id

    from ib_action.models import Action
    return Action.get_entities_with_user_action(**request_data)

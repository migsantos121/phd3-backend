def get_friends_actions_response(request_data, user, access_token):
    source = request_data["source"]
    entity_id = request_data["entity_id"]
    entity_type = request_data["entity_type"]
    action_type = request_data["action_type"]
    user_id = request_data["user_id"]
    user_type = request_data.get("user_type", "USER")
    limit = request_data.get("limit", 0)
    offset = request_data.get("offset", 0)

    from ib_action.models import Action
    friends_actions_response = Action.get_friends_actions(source=source, entity_id=entity_id, entity_type=entity_type,
                                                          user=user, limit=limit, offset=offset, user_type=user_type,
                                                          action_type=action_type, user_id=user_id,
                                                          access_token=access_token)
    return friends_actions_response

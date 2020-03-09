def api_wrapper(*args, **kwargs):
    user = kwargs["user"]
    request_data = kwargs["request_data"]
    request_data["user_id"] = user.id

    from ib_action.models import Action
    return Action.get_entities_with_user_actions(**request_data)

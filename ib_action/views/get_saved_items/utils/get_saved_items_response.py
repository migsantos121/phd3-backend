def get_saved_items_response(request_object, user):
    source = request_object["source"]
    action_type = request_object["action_type"]
    filter_entity_types = request_object["filter_entity_types"]
    offset = request_object.get("offset",0)
    limit = request_object.get("limit",0)

    from ib_action.models import Action
    response_object = Action.get_saved_items(source=source, user=user, action_type=action_type, offset=offset,
                                             limit=limit, filter_entity_types=filter_entity_types)
    return response_object

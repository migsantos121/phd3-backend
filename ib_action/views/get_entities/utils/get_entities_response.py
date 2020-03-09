
def get_entities_response(request_object, user):

    source = request_object["source"]
    entity_type = request_object["entity_type"]
    user_ids = request_object["user_ids"]

    from ib_action.models import Action
    response_object = Action.get_entities_with_summaries(source=source, user_ids=user_ids, entity_type=entity_type)
    return response_object
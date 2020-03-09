from ib_comments.models.comments import Comment


def get_comments_response(req_obj, user, access_token):
    entity_id = req_obj["entity_id"]
    entity_type = req_obj["entity_type"]
    offset = req_obj["offset"]
    limit = req_obj["limit"]
    search_q = req_obj['search_q']
    response_object = Comment.get_list_of_comments(entity_id=entity_id, entity_type=entity_type, offset=offset,
                                                   limit=limit, user=user, access_token=access_token, search_q=search_q)
    return response_object

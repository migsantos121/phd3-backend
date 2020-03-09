from ib_comments.models.comments import Comment


def count_of_comments_response(req_obj):
    entity_ids = []
    entity_types = []
    for each_object in req_obj:
        entity_id = each_object["entity_id"]
        entity_ids.append(entity_id)
        entity_type = each_object["entity_type"]
        entity_types.append(entity_type)

    comment_count_list = Comment.get_counts_of_comments(entity_ids, entity_types)
    return comment_count_list

import django.dispatch

comment_added = django.dispatch.Signal()


def save_comment_response(req_obj, user, access_token, source):
    entity_id = req_obj["entity_id"]
    entity_type = req_obj["entity_type"]
    comment = req_obj["comment"]
    multimedia = req_obj["multimedia"]
    multimedia_type = req_obj["multimedia_type"]

    from ib_comments.models.comments import Comment
    response_object, callback_dict = Comment.comment_on_entity(entity_id, entity_type, comment, multimedia,
                                                               multimedia_type, user, access_token, source)
    from ib_common.utilities.callback_wrapper import callback_wrapper
    callback_wrapper(source, 'ib_comments', 'save_comment', access_token, 1, callback_dict, comment_added, user)
    return response_object

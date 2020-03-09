from ib_comments.models.user_comment_vote import UserCommentVote


def vote_a_comment_response(req_obj, user, access_token=None, source=None):

    entity_id = req_obj["entity_id"]
    entity_type = req_obj["entity_type"]
    comment_id = req_obj["comment_id"]
    vote = req_obj["vote"]

    response_object, callback_dict = UserCommentVote.vote_a_comment(entity_id, entity_type, comment_id, vote, user, access_token=access_token)
    from ib_comments.views.vote_a_comment.callback_handler import callback_handler
    callback_handler(source, 'ib_comments', 'vote_a_comment_response', access_token, 1, callback_dict)
    return response_object

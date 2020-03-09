def delete_comment_response(request_object, user):
    comment_id = request_object["comment_id"]

    from ib_comments.models import Comment
    response_object = Comment.delete_comment(user_id=user.id, comment_id=comment_id)
    return response_object

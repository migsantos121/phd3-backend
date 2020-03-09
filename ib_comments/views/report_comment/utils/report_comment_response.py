from ib_comments.models.user_comment_report import UserCommentReport


def report_comment_response(req_obj, user):

    entity_id = req_obj["entity_id"]
    entity_type = req_obj["entity_type"]
    comment_id = req_obj["comment_id"]

    response_object = UserCommentReport.report_a_comment(entity_id, entity_type, comment_id, user)

    return response_object

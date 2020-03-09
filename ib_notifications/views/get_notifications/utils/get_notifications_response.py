from ib_notifications.models.notification import Notification


def get_notifications_response(request_object, user, access_token):
    limit = request_object["limit"]
    offset = request_object["offset"]
    source = request_object["source"]
    sort_by_date = request_object['sort_by_date']
    response_object = Notification.get_notifications_objects(source=source, offset=offset, limit=limit, sort_by_date=sort_by_date, user=user, access_token=access_token)
    return response_object

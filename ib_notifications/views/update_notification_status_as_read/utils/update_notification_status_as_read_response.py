from ib_notifications.models import Notification

def update_notification_status_as_read_response(request_data, user):
    notification_id = request_data["notification_id"]
    user_ids = request_data.get("user_ids", None)
    user_ids = [user.id] if not user_ids else user_ids
    response_object = Notification.update_notification_read_status(notification_id, user_ids)
    return response_object


def send_data_through_socket(title, message, extra_data, user_ids):
    real_time_data = {
        "title": title,
        "message": message,
        "extra_data": extra_data
    }

    for each_user_id in user_ids:
        from ib_notifications.utilities.send_real_time_data import send_real_time_data
        send_real_time_data(real_time_event = each_user_id, real_time_data=real_time_data)
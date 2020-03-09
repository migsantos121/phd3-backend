def send_real_time_data(request_data):
    from ib_notifications.utilities.send_real_time_data import send_real_time_data
    for data_obj in request_data:
        send_real_time_data(data_obj['real_time_event'], data_obj['real_time_data'])
    return

"""
Created on 26/12/16

@author: revanth
"""


def send_real_time_data(real_time_event, real_time_data):
    from ib_notifications.constants.general import dynamic_event_name
    from ib_notifications.utilities.socket_io_client import SocketIOClient
    from django.conf import settings

    socket_url = settings.SOCKET_URL
    socket_port = settings.SOCKET_PORT
    print 'socket_url: ', socket_url
    print 'socket_port: ', socket_port

    socketio_client = SocketIOClient(socket_url, socket_port)

    dynamic_event_data = {'eventName': real_time_event, 'eventData': real_time_data}

    socketio_client.emit_on_event(dynamic_event_name, dynamic_event_data)
    return

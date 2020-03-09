"""
Created on 26/12/16

@author: revanth
"""
from socketIO_client import SocketIO


def _callback(*args):
    print '_callback', args
    return


class SocketIOClient(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.socketio = SocketIO(self.hostname, self.port, wait_for_connection=False, verify=False)

    def get_client(self):
        return self.socketio

    def emit_on_event(self, event_name, data, callback=_callback):
        self.socketio.emit(event_name, data, callback)

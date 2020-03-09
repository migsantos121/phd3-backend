from requests.exceptions import HTTPError
from django.conf import settings
import requests
import json
from ib_notifications.utilities.abstract_cm_handler import AbstractCMHandler
from ib_notifications.constants.push_notification_types import PushNotificationTypes


__author__ = 'tanmay.ibhubs'


class FirebaseController(AbstractCMHandler):
    iid_url_batch_add = 'https://iid.googleapis.com/iid/v1:batchAdd'
    iid_url_batch_remove = 'https://iid.googleapis.com/iid/v1:batchRemove'
    fcm_send_data_url = 'https://fcm.googleapis.com/fcm/send'

    def __init__(self, *args, **kwargs):
        try:
            fcm_key_dict = settings.FCM_DJANGO_SETTINGS
            self.fcm_key = fcm_key_dict.get('FCM_SERVER_KEY', None)
            if self.fcm_key == None:
                raise NotImplementedError("FCM_SERVER_KEY not found in FCM_DJANGO_SETTINGS")
        except:
            raise NotImplementedError("FCM_DJANGO_SETTINGS not found in settings.py")

    def register_topic(self, channel_id, user_fcm_tokens):
        payload = {
            'to': '/topics/' + channel_id,
            'registration_tokens': user_fcm_tokens
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'key=' + self.fcm_key
        }
        response = requests.post(url=self.iid_url_batch_add, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            json_response = response.json()
            if not json_response['results']:
                return True
            else:
                return False

        raise HTTPError(response.reason)

    def unregister_topic(self, channel_id, user_fcm_tokens):
        raise NotImplementedError('This method is not implemented yet.')

    def send_data_to_topic(self, channel_id, title, message, extra_data):
        payload = {
            'to': '/topics/' + channel_id,
            'data': None
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'key=' + self.fcm_key
        }

        response = requests.post(url=self.fcm_send_data_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            pass

        raise HTTPError(response.reason)

    def send_data_to_multiple_user(self, receivers_token_list, title, message, extra_data, notification_type,
                                   push_notification_type=PushNotificationTypes.DATA.value):

        if not receivers_token_list:
            return True
        push_notification_type = self.clean_push_notification_type(push_notification_type=push_notification_type)
        if push_notification_type == PushNotificationTypes.DATA.value:
            notification_data = {
                'title': title,
                'message': message,
                'notification_type': notification_type,
                'extra_data': extra_data
            }

            payload = {
                'registration_ids': receivers_token_list,
                'data': notification_data
            }
        else:
            notification_data = {
                'title': title,
                'body': message,
            }

            payload = {
                'registration_ids': receivers_token_list,
                'notification': notification_data,
                'data': {
                    'notification_type': notification_type,
                    'extra_data': extra_data
                }
            }
        print payload

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'key=' + self.fcm_key
        }

        response = requests.post(url=self.fcm_send_data_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print "FCM RESPONSE FOR NOTIFICATION :", response.content
            return True

        raise HTTPError(response.reason)

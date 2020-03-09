from ib_notifications.utilities.abstract_cm_handler import AbstractCMHandler
from ib_notifications.constants.push_notification_types import PushNotificationTypes
from requests.exceptions import HTTPError
from django.conf import settings
import requests
import json

__author__ = 'tanmay.ibhubs'


class OneSignalController(AbstractCMHandler):
    def __init__(self, *args, **kwargs):
        try:
            onesignal_key_dict = settings.ONE_SIGNAL_DJANGO_SETTINGS
            self.auth_token = onesignal_key_dict.get('ONE_SIGNAL_AUTH_TOKEN', None)
            self.app_id = onesignal_key_dict.get('ONE_SIGNAL_APP_ID', None)
            if not self.auth_token or not self.app_id:
                raise NotImplementedError(
                    "ONE_SIGNAL_AUTH_TOKEN/ONE_SIGNAL_APP_ID not found in ONE_SIGNAL_DJANGO_SETTINGS")
        except:
            raise NotImplementedError("ONE_SIGNAL_DJANGO_SETTINGS not found in settings.py")

    def send_data_to_multiple_user(self, receivers_token_list, title, message, extra_data, notification_type,
                                   push_notification_type=PushNotificationTypes.DATA.value):
        if not receivers_token_list:
            receivers_token_list = []
        one_signal = self.get_one_signal()
        if title:
            title = {"en": title}

        notification_data = {
            'title': title,
            'message': message,
            'notification_type': notification_type,
            'extra_data': extra_data
        }

        data_dict = {
            "contents": message,
            "player_ids": receivers_token_list,
            "data": notification_data,
            "headings": title
        }

        non_keys = []
        for each_key in data_dict:
            if not data_dict[each_key]:
                non_keys.append(each_key)
        for each_key in non_keys:
            del data_dict[each_key]

        response = one_signal.create_notification(**data_dict)
        if response.status_code != 200:
            print response.content
            raise Exception("Error: Failed to send notification")
        else:
            try:
                print response.content
                response_dict = json.loads(response.content)
                errors = response_dict.get("errors")
                print errors, response_dict.get("id"), response_dict.get("recipients")
                if errors:
                    if isinstance(errors, list):
                        error_messages = " ".join(errors)
                        print "Failed to Send Nofication: %s" % error_messages
                    else:
                        invalid_player_ids = errors.get("invalid_player_ids", [])
                        if invalid_player_ids:
                            print "invalid_player_ids : ", errors["invalid_player_ids"]
            except Exception, err:
                print err

    def get_one_signal(self):
        from onesignal import OneSignal
        one_signal = OneSignal(self.auth_token, self.app_id)
        return one_signal

    def create_one_signal_player_id(self, device_type, device_id):
        one_signal = self.get_one_signal()
        res = one_signal.create_player(device_type=int(device_type), identifier=device_id)
        res_json = res.json()
        return res_json["id"]

    def edit_one_signal_player_id(self, player_id, tags):
        one_signal = self.get_one_signal()
        res = one_signal.edit_player(player_id=player_id, tags=tags)
        res_json = res.json()
        return res_json

    def register_topic(self, channel_id, user_fcm_tokens):
        pass

    def unregister_topic(self, channel_id, user_fcm_tokens):
        pass

    def send_data_to_topic(self, channel_id, title, message, extra_data):
        pass

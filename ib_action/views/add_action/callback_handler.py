"""
Created on 01/05/17

@author: revanth
"""
from django.dispatch import receiver
import django.dispatch

action_done = django.dispatch.Signal()


def callback_handler(source, app_name, operation_id, access_token, client_key_details_id, callback_dict):
    from django_swagger_utils.models import APICallback
    post_urls = APICallback.objects.filter(source=source, app_name=app_name, operation_id=operation_id).values_list(
        'post_url', flat=True)

    from ib_common.utilities.api_request import api_request
    for post_url in post_urls:
        headers_params = {"X-SOURCE": source}
        api_request(post_url, access_token, callback_dict, client_key_details_id, headers_params=headers_params)

    action_done.send_robust(None, **callback_dict)


# @receiver(action_done)
# def callback_receiver(sender, **kwargs):
#     print 'callback_handler: ', kwargs

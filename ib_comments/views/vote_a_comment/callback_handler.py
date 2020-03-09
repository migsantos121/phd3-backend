"""
Created on 05/05/17

@author: revanth
"""
import django.dispatch

comment_voted = django.dispatch.Signal()


def callback_handler(source, app_name, operation_id, access_token, client_key_details_id, callback_dict):
    from django_swagger_utils.models import APICallback
    post_urls = APICallback.objects.filter(source=source, app_name=app_name, operation_id=operation_id).values_list(
        'post_url', flat=True)

    from ib_common.utilities.api_request import api_request
    for post_url in post_urls:
        api_request(post_url, access_token, callback_dict, client_key_details_id)

    comment_voted.send_robust(None, **callback_dict)

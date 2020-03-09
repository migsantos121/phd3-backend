"""
Created on 01/05/17

@author: revanth
"""


def callback_wrapper(source, app_name, operation_id, access_token, client_key_details_id, callback_dict, signal_obj,
                     user=None):
    if callback_dict is None:
        callback_dict = {}
    from django_swagger_utils.models import APICallback
    post_urls = APICallback.objects.filter(source=source, app_name=app_name, operation_id=operation_id).values_list(
        'post_url', flat=True)

    print post_urls

    from ib_common.utilities.api_request import api_request
    for post_url in post_urls:
        api_request(post_url, access_token, callback_dict, client_key_details_id, source=source)

    if not callback_dict.get('access_token'):
        callback_dict['access_token'] = access_token
    if not callback_dict.get('source'):
        callback_dict['source'] = source
    if not callback_dict.get('user'):
        callback_dict['user'] = user
    signal_obj.send_robust(None, **callback_dict)

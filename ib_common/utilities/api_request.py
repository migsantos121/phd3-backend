"""
Created on 09/03/17

@author: revanth
"""
import requests
import json
import urllib

from ib_common.decorators.execution_time import execution_time


@execution_time()
def api_request(base_url, access_token, request_data, client_key_details_id, request_type='POST', path_params=None,
                query_params=None, headers_params=None, source=''):
    """Returns the json-encoded content of a response, if any.

        :param base_url: base_url to request to, of type string
        :param access_token: access_token for the api_request
        :param request_data: request data for the api_request
        :param client_key_details_id: client key details for the api_request
        :param request_type: optional request type argument can accept either POST or GET
        :raises ValueError: If the response body does not contain valid json.
        :raises InvalidRequestTypeException: request type argument is invalid
        :raises InvalidResponseTypeException: response is either none or of invalid type

    """
    url = base_url

    if path_params:
        url = url.format(**path_params)

    if query_params:
        url += "?" + urllib.urlencode(query_params, doseq=True)

    if headers_params is None:
        headers_params = {}

    request_data = json.dumps(json.dumps(request_data))
    # request_data = "'" + request_data + "'"
    data = {
        "clientKeyDetailsId": client_key_details_id,
        "data": request_data
    }
    json_data = json.dumps(data)

    if access_token is not None:
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}
    else:
        headers = {"Content-Type": "application/json"}

    headers.update(headers_params)

    if source:
        headers['x-source'] = source

    if request_type == 'POST':
        response = requests.post(url, data=json_data, headers=headers)
    elif request_type == 'PUT':
        response = requests.put(url, data=json_data, headers=headers)
    elif request_type == 'DELETE':
        response = requests.delete(url, data=json_data, headers=headers)
    elif request_type == 'GET':
        response = requests.get(url, headers=headers)
    else:
        from ib_common.exceptions.InvalidRequestTypeException import InvalidRequestTypeException
        raise InvalidRequestTypeException

    if response is None or type(response) != requests.Response:
        from ib_common.exceptions.InvalidResponseTypeException import InvalidResponseTypeException
        raise InvalidResponseTypeException

    from requests import HTTPError
    try:
        response.raise_for_status()
    except HTTPError as e:
        raise e

    if response.content:
        try:
            return response.json()
        except ValueError:
            raise ValueError
    else:
        return None

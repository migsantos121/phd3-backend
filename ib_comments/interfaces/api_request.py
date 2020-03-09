import requests
import json


def api_request(base_url, access_token, user_data):
    url = base_url
    user_data = json.dumps(user_data)
    user_data = " ' " + user_data + " ' "
    data = {
            "clientKeyDetailsId": 1,
            "data": user_data
    }
    jsondata = json.dumps(data)
    print url
    print jsondata

    if access_token is not None:
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}
    else:
        headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=jsondata, headers=headers)
    print response

    print response.json()

    return response.json()

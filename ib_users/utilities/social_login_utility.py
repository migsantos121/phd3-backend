import requests
from django.conf import settings
from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
# from phonenumbers.phonenumberutil import COUNTRY_CODE_TO_REGION_CODE
from twython import Twython

__author__ = 'tanmay.ibhubs'


def get_details_from_facebook(social_access_token):
    try:
        from open_facebook import OpenFacebook
        graph = OpenFacebook(access_token=social_access_token, version='v2.8')
        user = graph.get('me', fields='id, name, email')
        user['phone_number'] = None
        user['country_code'] = None
        user['name'] = user['name']
        return user
    except Exception as e:
        raise ExpectationFailed(str(e), res_status='failed')


def get_details_from_twitter(social_access_token, social_access_token_secret):
    try:
        twitter_app = settings.TWITTER
        app_key = twitter_app['app_key']
        app_secret = twitter_app['app_secret']
        twitter = Twython(app_key=app_key,
                          app_secret=app_secret,
                          oauth_token=social_access_token,
                          oauth_token_secret=social_access_token_secret)
        user = twitter.verify_credentials()
        user['phone_number'] = None
        user['name'] = user['screen_name']
        user['id'] = user['id_str']
        return user
    except Exception as e:
        raise ExpectationFailed(str(e), res_status='failed')


def get_details_from_google(social_access_token):
    authorization_header = {"Authorization": "OAuth %s" % social_access_token}
    request_object = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers=authorization_header,
                                  verify=False)
    google_plus_profile_details = request_object.json()
    if 'error' in google_plus_profile_details:
        raise ExpectationFailed(google_plus_profile_details['error'], res_status='failed')
    return google_plus_profile_details


def get_details_from_linkedin(social_access_token):
    try:
        import requests
        headers = {"Authorization": "Bearer %s" % social_access_token, "Connection": "Keep-Alive"}
        url = 'https://api.linkedin.com/v1/people/~:(id,email-address,first-name,last-name,date-of-birth,phone-numbers,positions,num-connections)?format=json'
        request_object = requests.get(url=url, headers=headers)
        request_content = request_object.content
        user = {}
        user['email'] = request_content.get('email', None)
        phone_numbers = request_content.get('phone-numbers', None)
        if phone_numbers:
            user['phone_number'] = phone_numbers[0]
        else:
            user['phone_number'] = None
        user['country_code'] = '+91'
        user['id'] = str(request_content['id'])
        user['name'] = request_content['formattedName'].replace(' ', '_')
        return user
    except Exception, err:
        print err
        message = str(err)
        raise ExpectationFailed('Internal Server Error - LinkedIn Login, %s' % message, res_status='failed')


def get_dialing_code_by_country(country):
    from ib_users.constants.country_code import country_calling_code
    return country_calling_code.get(country, '+91')

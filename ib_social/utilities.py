from django.conf import settings
from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
from twython import Twython

__author__ = 'tanmay.ibhubs'


def get_followers_ids_from_twitter(social_access_token, social_access_token_secret):
    twitter_app = settings.TWITTER
    app_key = twitter_app['app_key']
    app_secret = twitter_app['app_secret']
    twitter = Twython(app_key=app_key,
                      app_secret=app_secret,
                      oauth_token=social_access_token,
                      oauth_token_secret=social_access_token_secret)
    user_ids = []
    response = twitter.get_followers_ids(count=200)
    while 1:
        user_ids.extend(response['ids'])
        if response['next_cursor'] == 0:
            break
        response = twitter.get_followers_ids(count=200, cursor=response['next_cursor'])

    user_ids = map(str, user_ids)
    return user_ids


def get_friends_id_from_facebook(social_access_token):
    try:
        from open_facebook import OpenFacebook
        graph = OpenFacebook(access_token=social_access_token, version='v2.8')
        response = graph.get('me/friends/', count=100)
        fb_friends_dict = []
        while 1:
            friends = response['data']
            if not friends:
                break
            fb_friends_dict.extend(friends)
            cursor = response['paging']['cursors']['after']
            response = graph.get('me/friends/', count=100, after=cursor)

        return get_fb_friend_ids(fb_friends_dict)
    except:
        raise ExpectationFailed('Internal Server Error - FB Login', res_status='failed')


def get_fb_friend_ids(fb_friend_object):
    """
    
    :param fb_friend_object: [
                                {
                                  "name": "Subhadeep Dey",
                                  "id": "100002207343216"
                                },
                                {
                                  "name": "Vedavidh Budimuri",
                                  "id": "501861449919769"
                                }
                            ] 
    :return: ["100002207343216","501861449919769"]
    """

    fb_user_ids = [x['id'] for x in fb_friend_object]

    return fb_user_ids

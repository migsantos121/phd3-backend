from django.http import HttpResponse, response
from django.conf import settings
import oauth2 as oauth
import cgi
import json
from django.http import JsonResponse

consumer = oauth.Consumer('GamPkynWQpNms8ixyhnZQlVbH', 'E6MMRu9CNBf6IhQkNJaFsGamwd53d0wucoxJP5zzMj6nDQuc0Q')
client = oauth.Client(consumer)
request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authenticate_url = 'https://api.twitter.com/oauth/authenticate'
def twitter_request(request):
    resp, content = client.request(request_token_url, 'GET')
    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter.")
    request.session['request_token'] = dict(cgi.parse_qsl(content))
    data = request.session['request_token']
    return JsonResponse(data)


def get_twitter_response(request):
    token = oauth.Token(request.GET.get('oauth_token'), request.GET.get('oauth_verifier'))

    token.set_verifier(request.GET['oauth_verifier'])
    client = oauth.Client(consumer, token)
    resp, content = client.request(access_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter.")

    access_token = dict(cgi.parse_qsl(content))
    return JsonResponse(access_token)

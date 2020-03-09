from django.http.response import HttpResponse

__author__ = 'tanmay.ibhubs'


def api_wrapper(*args, **kwargs):
    user = kwargs['user']
    request_data = kwargs['request_data']
    social_provider = request_data['social_provider']

    access_token = kwargs.get('access_token', None)
    source = kwargs.get('source', '')
    from ib_social.models import MemberRelation

    MemberRelation.delink_user_social_account(user=user, social_provider=social_provider,
                                              access_token=access_token, source=source)
    return HttpResponse()

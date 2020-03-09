import os


class CommonInterface():
    def __init__(self, user, access_token, request_type, source=''):
        self.user = user
        self.source = source
        self.access_token = access_token
        self.request_type = request_type
        self.branch = os.environ.get('DJANGO_SETTINGS_MODULE').split('.')[2]
        self.base_url = self.get_url()

    def get_url(self):
        from django.conf import settings
        base_url = getattr(settings, 'IB_COMMENTS_APIGATEWAY_ENDPOINT', '')
        return base_url + 'api/ib_comments/'

    def get_comments(self,entity_id,entity_type,offset,limit):
        request_data = dict([
            ('entity_id', entity_id),
            ('entity_type', entity_type),
            ('offset', offset),
            ('limit', limit)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'get_comments/'
            from ib_comments.interfaces.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          user_data=request_data)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_comments.views.get_comments.utils.get_comments_response import get_comments_response
            return get_comments_response(request_data,self.user,self.access_token)
        else:
            pass

    def report_comment(self, entity_id, entity_type, comment_id):
        request_data = dict([
            ('entity_id', entity_id),
            ('entity_type', entity_type),
            ('comment_id', comment_id)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'report_comment/'
            from ib_comments.interfaces.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          user_data=request_data)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_comments.views.report_comment.utils.report_comment_response import report_comment_response
            return report_comment_response(request_data, self.user)
        else:
            pass

    def save_comment(self, entity_id, entity_type,comment,multimedia,multimedia_type):
        request_data = dict([
            ('entity_id', entity_id),
            ('entity_type', entity_type),
            ('comment', comment),
            ('multimedia', multimedia),
            ("multimedia_type",multimedia_type),
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'save_comment/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=self.source)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_comments.views.save_comment.utils.save_comment_response import save_comment_response
            return save_comment_response(request_data, self.user,self.access_token, self.source)
        else:
            pass

    def vote_a_comment(self, entity_id, entity_type, comment_id, vote):
        request_data = dict([
            ('entity_id', entity_id),
            ('entity_type', entity_type),
            ('comment_id', comment_id),
            ('vote', vote)
        ])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'vote_a_comment/'
            from ib_comments.interfaces.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          user_data=request_data)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_comments.views.vote_a_comment.utils.vote_a_comment_response import vote_a_comment_response
            return vote_a_comment_response(request_data, self.user)
        else:
            pass
    def get_count_of_comments(self,entity_list):

        if self.request_type == 'SERVICE':
            url = self.base_url + 'get_count_of_comments/'
            from ib_comments.interfaces.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          user_data=entity_list)
            return response_object
        elif self.request_type == 'LIBRARY':
            from ib_comments.views.get_count_of_comments.utils.get_count_of_comments_response import count_of_comments_response
            return count_of_comments_response(entity_list)
        else:
            pass

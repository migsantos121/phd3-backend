from django_swagger_utils.drf_server.decorators.handle_exceptions import handle_exceptions
from ib_common.interface_utils.interface_utils import InterfaceUtils

__author__ = 'ibhubs'


class IBPostsServiceInterface(InterfaceUtils):
    def __init__(self, *args, **kwargs):
        super(IBPostsServiceInterface, self).__init__(*args, **kwargs)

    @property
    def service_flag(self):
        from django.conf import settings
        from ib_common.constants.service_types import ServiceTypesEnum
        return getattr(settings, 'IB_POSTS_REQUEST_TYPE', ServiceTypesEnum.LIBRARY.value)

    @property
    def service_base_url(self):
        from django.conf import settings
        return self.clean_base_url(getattr(settings, 'IB_POSTS_BASE_URL', '')) + 'api/ib_posts/'

    @property
    def client_key_details_id(self):
        return 1

    @handle_exceptions()
    def add_post(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'article/add_post/')

        def api_wrapper(*args, **kwargs):
            from ib_posts.views.add_post.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def update_post(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'posts/{post_id}/')

        def api_wrapper(*args, **kwargs):
            from ib_posts.views.update_post.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def delete_post(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'DELETE')
        setattr(self, 'url_tail', 'posts/{post_id}/')

        def api_wrapper(*args, **kwargs):
            from ib_posts.views.delete_post.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def get_post(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'GET')
        setattr(self, 'url_tail', 'posts/{post_id}/')

        def api_wrapper(*args, **kwargs):
            from ib_posts.views.get_post.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def get_posts_by_user_id(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'user/posts/')

        def api_wrapper(*args, **kwargs):
            from ib_posts.views.get_posts_by_user_id.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def get_posts(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'posts/')

        def api_wrapper(*args, **kwargs):
            from ib_posts.views.get_posts.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def get_post_with_article(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'GET')
        setattr(self, 'url_tail', 'posts/{post_id}/article/')

        def api_wrapper(*args, **kwargs):
            from ib_posts.views.get_post_with_article.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def get_post_user_stats(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'GET')
        setattr(self, 'url_tail', '/user/posts/stats/')

        def api_wrapper(*args, **kwargs):
            from ib_posts.views.get_post_user_stats.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

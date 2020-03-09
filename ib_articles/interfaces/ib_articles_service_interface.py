from django_swagger_utils.drf_server.decorators.handle_exceptions import handle_exceptions
from ib_common.interface_utils.interface_utils import InterfaceUtils

__author__ = 'ibhubs'


class IBArticlesServiceInterface(InterfaceUtils):
    def __init__(self, *args, **kwargs):
        super(IBArticlesServiceInterface, self).__init__(*args, **kwargs)

    @property
    def service_flag(self):
        from django.conf import settings
        from ib_common.constants.service_types import ServiceTypesEnum
        return getattr(settings, 'IB_ARTICLES_REQUEST_TYPE', ServiceTypesEnum.LIBRARY.value)

    @property
    def service_base_url(self):
        from django.conf import settings
        return self.clean_base_url(getattr(settings, 'IB_ARTICLES_BASE_URL', '')) + 'api/ib_articles/'

    @property
    def client_key_details_id(self):
        return 1

    @handle_exceptions()
    def add_article(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'article/add_article/')

        def api_wrapper(*args, **kwargs):
            from ib_articles.views.add_article.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def update_article(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'article/{article_id}/')

        def api_wrapper(*args, **kwargs):
            from ib_articles.views.update_article.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def delete_article(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'DELETE')
        setattr(self, 'url_tail', 'article/{article_id}/')

        def api_wrapper(*args, **kwargs):
            from ib_articles.views.delete_article.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def get_article(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'GET')
        setattr(self, 'url_tail', 'article/{article_id}/')

        def api_wrapper(*args, **kwargs):
            from ib_articles.views.get_article.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def get_article_by_ids(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'article/get_article_by_ids/')

        def api_wrapper(*args, **kwargs):
            from ib_articles.views.get_article_by_ids.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def get_articles(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'article/articles/')

        def api_wrapper(*args, **kwargs):
            from ib_articles.views.get_articles.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def get_article_keyword_maps(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'article/keyword_maps/')

        def api_wrapper(*args, **kwargs):
            from ib_articles.views.get_article_keyword_maps.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def get_basic_articles(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'article/basic/')

        def api_wrapper(*args, **kwargs):
            from ib_articles.views.get_basic_articles.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def get_keywords(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'keywords/')

        def api_wrapper(*args, **kwargs):
            from ib_articles.views.get_keywords.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

    @handle_exceptions()
    def add_news_source(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'news_sources/')

        def api_wrapper(*args, **kwargs):
            from ib_articles.views.add_news_source.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()


    @handle_exceptions()
    def add_keywords(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'keywords/add_keywords/')

        def api_wrapper(*args, **kwargs):
            from ib_articles.views.add_keywords.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

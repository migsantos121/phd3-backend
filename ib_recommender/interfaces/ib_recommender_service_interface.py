from django_swagger_utils.drf_server.decorators.handle_exceptions import handle_exceptions
from ib_common.interface_utils.interface_utils import InterfaceUtils

__author__ = 'ibhubs'


class IBRecommenderServiceInterface(InterfaceUtils):
    def __init__(self, *args, **kwargs):
        super(IBRecommenderServiceInterface, self).__init__(*args, **kwargs)

    @property
    def service_flag(self):
        from django.conf import settings
        from ib_common.constants.service_types import ServiceTypesEnum
        return getattr(settings, 'IB_RECOMMENDER_REQUEST_TYPE', ServiceTypesEnum.LIBRARY.value)

    @property
    def service_base_url(self):
        from django.conf import settings
        return self.clean_base_url(getattr(settings, 'IB_RECOMMENDER_BASE_URL', '')) + 'api/ib_recommender/'

    @property
    def client_key_details_id(self):
        return 1

    @handle_exceptions()
    def get_articles(self, request_data=None, path_params=None, query_params=None, headers_obj=None, **kwargs):
        setattr(self, 'request_data', request_data)
        setattr(self, 'path_params', path_params)
        setattr(self, 'query_params', query_params)
        setattr(self, 'headers_obj', headers_obj)
        setattr(self, 'request_type', 'POST')
        setattr(self, 'url_tail', 'articles/')

        def api_wrapper(*args, **kwargs):
            from ib_recommender.views.get_articles.api_wrapper import api_wrapper
            return api_wrapper(*args, **kwargs)

        setattr(self, 'api_wrapper', api_wrapper)
        return self.execute()

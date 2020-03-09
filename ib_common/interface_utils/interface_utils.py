from abc import ABCMeta
from abc import abstractproperty

__author__ = 'vedavidh'


class InterfaceUtils(object):
    def __init__(self, user, access_token, source=''):
        self.user = user
        self.access_token = access_token
        self.source = source

    __metaclass__ = ABCMeta

    @abstractproperty
    def service_flag(self):
        pass

    @abstractproperty
    def service_base_url(self):
        pass

    @abstractproperty
    def client_key_details_id(self):
        pass

    @classmethod
    def clean_base_url(cls, base_url):
        return base_url + "/" if base_url[-1] != "/" else base_url

    def send_request(self, request_type):

        from ib_common.utilities.api_request import api_request
        setattr(self, 'url', self.service_base_url + self.url_tail)
        response = api_request(
            access_token=self.access_token,
            base_url=self.url,
            request_data=self.request_data,
            client_key_details_id=self.client_key_details_id,
            request_type=request_type,
            path_params=self.path_params,
            query_params=self.query_params,
            headers_params=self.headers_params,
            source=self.source
        )
        return response

    def execute(self):

        path_params = getattr(self, 'path_params', {})
        setattr(self, 'path_params', path_params if path_params is not None else {})
        query_params = getattr(self, 'query_params', {})
        setattr(self, 'query_params', query_params if query_params is not None else {})
        headers_params = getattr(self, 'headers_params', {})
        setattr(self, 'headers_params', headers_params if headers_params is not None else {})

        from ib_common.constants.service_types import ServiceTypesEnum
        if self.service_flag == ServiceTypesEnum.SERVICE.value:
            response = self.send_request(self.request_type)
        else:
            if not self.source:
                self.source = self.headers_params.get('x-source', '')

            kwargs = {
                "request_headers_obj": self.headers_params,
                "request_query_params": self.query_params,
                "source": self.source
            }
            kwargs.update(self.path_params)
            response = self.api_wrapper(request_data=self.request_data, user=self.user, access_token=self.access_token,
                                        **kwargs)
        return response

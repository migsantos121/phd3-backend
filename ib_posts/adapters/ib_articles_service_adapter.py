from ib_common.service_adapter_utils.base_adapter_class import BaseAdapterClass

__author__ = 'vedavidh'


class IBArticlesServiceAdapter(BaseAdapterClass):
    def __init__(self, *args, **kwargs):
        super(IBArticlesServiceAdapter, self).__init__(*args, **kwargs)

    @property
    def conn(self):
        from ib_articles.interfaces.ib_articles_service_interface import IBArticlesServiceInterface
        _interface = IBArticlesServiceInterface(self.user, self.access_token)
        return _interface

    def get_article_by_ids(self, article_ids, offset, limit):
        request_data = {
            "search_q": "",
            "limit": limit,
            "filters": {
                "sorts": {
                    "published_time": "desc"
                },
                "article_ids": article_ids
            },
            "offset": offset
        }
        response = self.conn.get_article_by_ids(request_data=request_data)
        return response

    def get_article(self, article_id):
        path_params = {
            "article_id": article_id
        }
        response = self.conn.get_article(path_params=path_params)
        return response

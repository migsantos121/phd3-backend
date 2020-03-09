from ib_common.service_adapter_utils.base_adapter_class import BaseAdapterClass

__author__ = 'vedavidh'


class IBRecommenderServiceAdapter(BaseAdapterClass):
    def __init__(self, *args, **kwargs):
        super(IBRecommenderServiceAdapter, self).__init__(*args, **kwargs)

    @property
    def conn(self):
        from ib_recommender.interfaces.ib_recommender_service_interface import IBRecommenderServiceInterface
        _interface = IBRecommenderServiceInterface(self.user, self.access_token)
        return _interface

    def get_articles(self, keyword_ids=None, category_ids=None):
        if keyword_ids is None:
            keyword_ids = []
        if category_ids is None:
            category_ids = []
        request_data = {
            "keyword_ids": keyword_ids,
            "category_ids": category_ids
        }
        response = self.conn.get_articles(request_data=request_data)
        return response

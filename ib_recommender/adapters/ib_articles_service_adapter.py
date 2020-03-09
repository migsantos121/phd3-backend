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

    def get_article_article_keyword_maps(self, keyword_ids):
        request_data = {
            "keyword_ids": keyword_ids
        }
        response = self.conn.get_article_keyword_maps(request_data=request_data)
        return response

    def get_basic_articles(self, article_ids, end_published_time="", start_published_time="",
                           sort_by_published_date="desc"):
        request_data = {
            "sorts": {
                "posted_date": "string",
                "published_time": sort_by_published_date
            },
            "published_time": {
                "start_date_time": start_published_time,
                "end_date_time": end_published_time
            },
            "article_ids": article_ids
        }
        response = self.conn.get_basic_articles(request_data=request_data)
        return response

    def get_keywords(self, keyword_ids=None, search_q=None, limit=0, offset=0):
        if search_q is None:
            search_q = ""
        if keyword_ids is None:
            keyword_ids = []
        request_data = {
            "search_q": search_q,
            "keyword_ids": keyword_ids,
            "limit": limit,
            "offset": offset
        }
        response = self.conn.get_keywords(request_data=request_data)
        return response

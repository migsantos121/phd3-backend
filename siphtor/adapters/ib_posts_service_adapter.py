from ib_common.service_adapter_utils.base_adapter_class import BaseAdapterClass

__author__ = 'vedavidh'


class IBPostsServiceAdapter(BaseAdapterClass):
    def __init__(self, *args, **kwargs):
        super(IBPostsServiceAdapter, self).__init__(*args, **kwargs)

    @property
    def conn(self):
        from ib_posts.interfaces.ib_posts_service_interface import IBPostsServiceInterface
        _interface = IBPostsServiceInterface(self.user, self.access_token)
        return _interface

    def get_posts(self, post_ids, user_ids, offset, limit):
        request_data = {
            "search_q": "",
            "offset": offset,
            "filters": {
                "sorts": {
                    "posted_date": "desc"
                },
                "post_ids": post_ids,
                "user_ids": user_ids,
                "include_article_info": True
            },
            "limit": limit
        }
        response = self.conn.get_posts(request_data=request_data)
        return response

    def get_user_posts(self, offset, limit, media_types):
        request_data = {
            "search_q": "",
            "offset": offset,
            "filters": {
                "sorts": {
                    "posted_date": "desc"
                },
                "include_article_info": True,
                "media_types": media_types
            },
            "limit": limit,
        }
        response = self.conn.get_posts_by_user_id(request_data=request_data)
        return response

    def get_post_user_stats(self):
        response = self.conn.get_post_user_stats()
        return response

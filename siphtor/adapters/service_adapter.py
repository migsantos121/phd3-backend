from ib_common.service_adapter_utils.base_adapter_class import BaseAdapterClass

__author__ = 'vedavidh'


class ServiceAdapter(BaseAdapterClass):
    def __init__(self, *args, **kwargs):
        super(ServiceAdapter, self).__init__(*args, **kwargs)

    @property
    def ib_users(self):
        from .ib_users_service_adapter import IBUsersServiceAdapter
        return IBUsersServiceAdapter(access_token=self.access_token, user=self.user)

    @property
    def ib_articles(self):
        from .ib_articles_service_adapter import IBArticlesServiceAdapter
        return IBArticlesServiceAdapter(access_token=self.access_token, user=self.user)

    @property
    def ib_recommender(self):
        from .ib_recommender_service_adapter import IBRecommenderServiceAdapter
        return IBRecommenderServiceAdapter(access_token=self.access_token, user=self.user)

    @property
    def ib_actions(self):
        from .ib_actions_service_adapter import IBActionsServiceAdapter
        return IBActionsServiceAdapter(access_token=self.access_token, user=self.user)

    @property
    def ib_comments(self):
        from .ib_comments_service_adapter import IBCommentsServiceAdapter
        return IBCommentsServiceAdapter(access_token=self.access_token, user=self.user)

    @property
    def ib_posts(self):
        from .ib_posts_service_adapter import IBPostsServiceAdapter
        return IBPostsServiceAdapter(access_token=self.access_token, user=self.user)

    @property
    def ib_social(self):
        from .ib_social_service_adapter import IBSocialServiceAdapter
        return IBSocialServiceAdapter(access_token=self.access_token, user=self.user)

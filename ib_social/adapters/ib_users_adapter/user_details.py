from ib_social.adapters.base_adapter_class import BaseAdapterClass

__author__ = 'tanmay.ibhubs'


class UserDetails(BaseAdapterClass):
    def __init__(self, *args, **kwargs):
        self.request_type = kwargs.pop('request_type')
        super(UserDetails, self).__init__(*args, **kwargs)

    def get_usp_by_social_ids(self, social_ids, social_provider):
        try:
            from ib_users.interfaces.CommonInterface import CommonInterface
            user_interface = CommonInterface(self.user, self.access_token, self.request_type)
            response = user_interface.get_usp_details(social_ids, social_provider)
            print "Social Object", response
            return response
        except Exception as err:
            print 'IB User Error--->', err

            from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
            raise ExpectationFailed('Internal Server Error: ib_users',
                                    res_status=False)

    def link_user_social_account(self, social_provider=None, social_token=None,
                                 social_access_token_secret=None,
                                 source=None):
        try:
            from ib_users.interfaces.CommonInterface import CommonInterface
            user_interface = CommonInterface(self.user, self.access_token, self.request_type)
            response = user_interface.link_user_social_profile(social_provider=social_provider,
                                                               social_token=social_token,
                                                               social_access_token_secret=social_access_token_secret,
                                                               source=source)
            print "Social Object for linking", response
            return response
        except Exception as err:
            print 'IB User Error--->', err

            from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
            raise ExpectationFailed('Internal Server Error: Social account linking failed in ib_users',
                                    res_status=False)

    def delink_user_social_account(self, social_provider=None, source=''):
        try:
            from ib_users.interfaces.CommonInterface import CommonInterface
            user_interface = CommonInterface(self.user, self.access_token, self.request_type)
            response = user_interface.delink_user_social_profile(social_provider=social_provider, source=source)
            return response
        except Exception as err:
            print 'IB User Error--->', err

            from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
            raise ExpectationFailed('Internal Server Error: Social account de-linking failed in ib_users',
                                    res_status=False)

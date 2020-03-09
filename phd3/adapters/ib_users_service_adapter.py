from ib_common.service_adapter_utils.base_adapter_class import BaseAdapterClass

__author__ = 'vedavidh'


class IBUsersServiceAdapter(BaseAdapterClass):
    def __init__(self, *args, **kwargs):
        from django.conf import settings
        self.request_type = settings.IB_USERS_REQUEST_TYPE
        self.source = settings.IB_USERS_SOURCE
        super(IBUsersServiceAdapter, self).__init__(*args, **kwargs)

    @property
    def conn(self):
        from ib_users.interfaces.CommonInterface import CommonInterface
        user_interface = CommonInterface(self.user, self.access_token, self.request_type, self.source)
        return user_interface

    def get_users(self, user_ids, search_q, exclude_user_ids, offset=None, limit=None):
        response = self.conn.get_users(user_ids, search_q, exclude_user_ids, offset=offset, limit=limit)
        users_list = []
        for each in response:
            users_list.append(self.convert_user_details_dict_to_profile(each))
        return users_list

    @staticmethod
    def convert_user_details_dict_to_profile(response_dict):
        user_profile = {
            "user_id": response_dict["m_id"],
            "profile_pic": response_dict["m_pic"],
            "gender": response_dict["m_gender"],
            "name": response_dict["m_name"],
            "dob": response_dict["dob"],
            "phone_number": response_dict["m_phone_number"],
            "email": response_dict["m_email"],
            "country_code": response_dict["m_country_code"],
            "username": response_dict["m_username"],
            "extra_details": response_dict["extra_details"],
        }
        return user_profile

import os

from django_swagger_utils.drf_server.decorators.handle_exceptions import handle_exceptions


class CommonInterface(object):
    def __init__(self, user, access_token, request_type, source=''):
        self.source = source
        self.user = user
        self.access_token = access_token
        self.request_type = request_type
        self.branch = os.environ.get('DJANGO_SETTINGS_MODULE').split('.')[2]
        self.base_url = self.get_url()

    def get_url(self):
        from django.conf import settings
        base_url = getattr(settings, 'IB_USERS_BASE_URL', '')
        return base_url + 'api/ib_users/'

    def get_access_credentials_with_pwd(self, username, password, client_id, client_secret, scopes='read write'):
        request_data = {'username': username, 'password': password, 'client_id': client_id,
                        'client_secret': client_secret, 'scopes': scopes}
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/access_credentials/pwd/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def check_user_in_group(self, user_id):
        request_data = dict([('user_id', user_id)])
        if self.request_type == 'SERVICE':
            url = self.base_url + 'discussion/user/group/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)

            return response_object
        else:
            pass

    def create_users(self, member_details, source):
        member_data = list()
        for member in member_details:
            if 'dob' in member.keys():
                dob = member['dob']
            else:
                dob = ''
            member_detail = dict([('m_username', member['username']),
                                  ('m_pic', member['pic']), ('m_name', member['name']),
                                  ('is_admin', member['is_admin']), ('dob', dob)])
            member_data.append(member_detail)

        request_data = dict([('member_details', member_data), ('source', source)])

        if self.request_type == 'SERVICE':
            url = self.base_url + 'group/user/create/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)

            return response_object
        else:
            pass

    def get_user_details_by_id(self, user_ids, source):

        request_data = dict([('user_ids', user_ids)])
        print 'Request Data--->', request_data

        if self.request_type == 'SERVICE':
            url = self.base_url + 'users/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=source)
            print 'Response Object--->', response_object
            return response_object
        else:
            pass

    def get_user_details_by_usernames(self, usernames, source):
        request_data = dict()
        request_data['usernames'] = usernames

        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/usernames/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=source)

            return response_object
        else:
            pass

    def get_user_details_with_social_details(self, source):
        request_data = dict()

        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=source)

            return response_object
        else:
            pass

    def get_username(self, user_id):
        request_data = dict([('user_id', user_id)])

        if self.request_type == 'SERVICE':
            url = self.base_url + 'username/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)

            return response_object
        else:
            pass

    def modify_user_details(self, user_id, is_lazy_deleted, group, permission_details):
        request_data = dict([('user_id', user_id), ('is_lazy_deleted', is_lazy_deleted),
                             ('group', group), ('permission_details', permission_details)])

        if self.request_type == 'SERVICE':
            url = self.base_url + 'discussion/permission/user/modify/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)

            return response_object
        else:
            pass

    def validate_user_id(self, user_ids):
        # TODO: need to write an API, when used as SERVICE
        request_data = dict([('user_ids', user_ids)])

        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/validate/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)

            return response_object
        else:
            pass

    def validate_users_credentials_and_get_user_details(self, users_credentials):
        # TODO: need to write an API, when used as SERVICE
        request_data = dict([('users_credentials', users_credentials)])

        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/validate/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)

            return response_object
        else:
            pass

    def login_or_register_with_username(self, username, password, name, email, phone_number):
        request_data = {'username': username, 'password': password, 'name': name, 'email': email,
                        'phone_number': password}
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/login/custom_username/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def get_user_id_from_username(self, username, password):
        request_data = {'username': username, 'password': password}
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/user_id/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def get_names_from_userids(self, user_ids):
        request_data = {'user_ids': user_ids}
        if self.request_type == 'SERVICE':
            url = self.base_url + 'users/name/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def login_user_v2(self, auth_type=None, password=None, username=None, phone_number=None, email=None,
                      country_code=None, client_id=None, client_secret=None, scopes='read write'):
        request_data = {
            "auth_type": auth_type,
            "username": username,
            "email": email,
            "password": password,
            "client_id": client_id,
            "client_secret": client_secret,
            "country_code": country_code,
            "phone_number": phone_number
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/login/v2/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def register_user_v2(self, reg_type=None, password=None, dob=None, gender=None, phone_number=None, email=None,
                         country_code=None, username=None, pic=None, pic_thumbnail=None, registration_source=None,
                         first_name=None, last_name=None, name=None):
        request_data = {
            "reg_type": reg_type,
            "password": password,
            "dob": dob,
            "gender": gender,
            "phone_number": phone_number,
            "email": email,
            "country_code": country_code,
            "username": username,
            "pic": pic,
            "pic_thumbnail": pic_thumbnail,
            "registration_source": registration_source,
            "fist_name": first_name,
            "last_name": last_name,
            "name": name
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/register/v2/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def recover_user_password_v2(self, auth_type=None, username=None, email=None, client_id=None, client_secret=None,
                                 country_code=None, phone_number=None):

        request_data = {
            "auth_type": auth_type,
            "username": username,
            "email": email,
            "client_id": client_id,
            "client_secret": client_secret,
            "country_code": country_code,
            "phone_number": phone_number
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/recover_password/v2/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def reset_user_password_v2(self, auth_type=None, username=None, email=None, password=None, token=None,
                               client_id=None,
                               client_secret=None, country_code=None,
                               phone_number=None):
        request_data = {
            "auth_type": auth_type,
            "username": username,
            "email": email,
            "password": password,
            "token": token,
            "client_id": client_id,
            "client_secret": client_secret,
            "country_code": country_code,
            "phone_number": phone_number
        }

        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/reset_password/v2/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def update_user_data_v2(self, fields):
        request_data = fields

        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/update_data/v2/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def verify_data_update_pre_login_v2(self, auth_type=None, email=None, country_code=None, phone_number=None,
                                        verify_token=None, client_id=None, client_secret=None):
        request_data = {
            "auth_type": auth_type,
            "email": email,
            "country_code": country_code,
            "phone_number": phone_number,
            "verify_token": verify_token,
            "client_id": client_id,
            "client_secret": client_secret
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/verify_data_update_pre_login/v2/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def verify_data_update_v2(self, auth_type=None, email=None, country_code=None, phone_number=None,
                              verify_token=None, user=None):
        request_data = {
            "auth_type": auth_type,
            "email": email,
            "country_code": country_code,
            "phone_number": phone_number,
            "verify_token": verify_token
        }

        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/verify_data_update/v2/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def activate_or_deactivate_account(self, make_active=None):
        request_data = {
            'make_active': make_active
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/activate_or_deactivate_account/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def social_login(self, provider=None, social_provider_token=None, social_provider_token_secret=None, client_id=None,
                     client_secret=None):
        request_data = {
            'provider': provider,
            'social_provider_token': social_provider_token,
            'social_provider_token_secret': social_provider_token_secret,
            'client_id': client_id,
            'client_secret': client_secret
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/social_login/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def user_logout(self):
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/user_logout/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=None, request_type="GET",
                                          client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def user_logout_from_device(self, device_id, device_type):
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/user_logout/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data={'device_id': device_id, 'device_type': device_type},
                                          request_type="POST", client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def delete_user(self):
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/user_logout/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=None, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def set_password(self, password):
        request_data = {
            'password': password
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/set_password/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def set_language(self, language):
        request_data = {
            'language': language
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/set_language/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def get_usp_details(self, social_ids, social_provider):
        request_data = {
            'social_ids': social_ids,
            'social_provider': social_provider
        }

        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/get_social_details/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    @handle_exceptions()
    def get_usp_detail(self, social_provider):
        request_data = {
            'social_provider': social_provider
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/get_social_detail/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def update_user_details_by_others(self, req_data):
        request_data = req_data
        if self.request_type == 'SERVICE':
            url = self.base_url + 'external/user/update/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def get_minimal_details(self, source):
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/minimal_details/'
            from ib_common.utilities.api_request import api_request
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=None, client_key_details_id=1, source=source)
            return response_object
        else:
            pass

    def get_minimal_details_by_user_ids(self, user_ids, source):
        request_data = {
            'user_ids': user_ids
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'users/minimal_details/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=source)
            return response_object
        else:
            pass

    def update_password(self, old_password, new_password):
        request_data = {
            'old_password': old_password,
            'new_password': new_password
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/access_credentials/pwd/update/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1)
            return response_object
        else:
            pass

    def get_users(self, user_ids, search_q, exclude_user_ids, source, offset=None, limit=None):
        request_data = {
            'user_ids': user_ids,
            'search_q': search_q,
            'exclude_user_ids': exclude_user_ids,
            'offset': offset,
            'limit': limit
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'users/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=source)
            return response_object
        else:
            pass

    def link_user_social_profile(self, social_provider=None, social_token=None,
                                 social_access_token_secret=None,
                                 source=None):
        request_data = {
            "social_provider": social_provider,
            "social_token": social_token,
            "social_access_token_secret": social_access_token_secret,
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/link_social_account/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=source)
            return response_object
        else:
            pass

    def get_user_detail_by_auth_type(self, auth_type=None, email=None, phone_number=None, country_code=None,
                                     username=None, source=None):
        request_data = {
            'auth_type': auth_type,
            'email': email,
            'phone_number': phone_number,
            'country_code': country_code,
            'username': username
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/get_user_by_auth_type/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=source)
            return response_object
        else:
            pass

    def check_username_availability(self, username=None, source=''):
        request_data = {
            'username': username
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/availability/username/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=source)
            return response_object
        else:
            pass

    def delink_user_social_account(self, social_provider=None, social_token=None,
                                   social_access_token_secret=None,
                                   source=None):
        request_data = {
            "social_provider": social_provider,
            "social_token": social_token,
            "social_access_token_secret": social_access_token_secret,
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/delink_social_account/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=source)
            return response_object
        else:
            pass

    def get_user(self, source=''):
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          client_key_details_id=1, source=source, request_data=None)
            return response_object
        else:
            pass

    def update_user_details(self, user_details=None, source=''):
        request_data = {
            "user_details": user_details,
            "source": source
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/update/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=source)
            return response_object
        else:
            pass

    def search_user_by_auth_type(self, auth_type=None, username=None, phone_number=None, email=None, country_code=None):
        request_data = {
            "auth_type": auth_type,
            "username": username,
            "email": email,
            "country_code": country_code,
            "phone_number": phone_number
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/search_by_auth_type/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=self.source)
            return response_object
        else:
            pass

    def resend_otp_v2_for_data_verification(self, auth_type=None,  phone_number=None, email=None, country_code=None):
        request_data = {
            "auth_type": auth_type,
            "email": email,
            "country_code": country_code,
            "phone_number": phone_number
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/auth/update/otp/resend/v2/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=self.source)
            return response_object
        else:
            pass

    def user_login_v2_with_otp(self, auth_type=None,  phone_number=None, email=None, country_code=None):
        request_data = {
            "auth_type": auth_type,
            "email": email,
            "country_code": country_code,
            "phone_number": phone_number
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + 'user/login/otp/v2/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=self.source)
            return response_object
        else:
            pass

    def user_login_v2_verify_otp(self, auth_type=None, phone_number=None, email=None, country_code=None,
                                 client_secret=None, client_id=None,
                                 verify_token=None, scopes='read write update delete'):
        request_data = {
            "auth_type": auth_type,
            "client_secret": client_secret,
            "client_id": client_id,
            "verify_token": verify_token,
            "scopes": scopes,
            "email": email,
            "country_code": country_code,
            "phone_number": phone_number
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + '/user/login/otp/verify/v2/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=self.source)
            return response_object
        else:
            pass

    def resend_otp_v2_for_verified_auth(self, auth_type=None,  phone_number=None, email=None, country_code=None):
        request_data = {
            "auth_type": auth_type,
            "email": email,
            "country_code": country_code,
            "phone_number": phone_number
        }
        if self.request_type == 'SERVICE':
            url = self.base_url + '/user/login/otp/resend/v2/'
            from ib_common.utilities.api_request import api_request
            response_object = api_request(base_url=url, access_token=self.access_token,
                                          request_data=request_data, client_key_details_id=1, source=self.source)
            return response_object
        else:
            pass

import os

from django_swagger_utils.drf_server.decorators.handle_exceptions import handle_exceptions

from ib_users.models.user_social_provider import UserSocialProvider


class CommonInterface(object):
    def __init__(self, user, access_token, request_type, source=''):
        self.source = source
        self.user = user
        self.access_token = access_token
        self.request_type = request_type
        self.branch = os.environ.get('DJANGO_SETTINGS_MODULE').split('.')[2]
        self.interface_service = self.make_interface_service_call()

    def make_interface_service_call(self):
        from ib_users.interfaces.interface_service.CommonInterfaceService import CommonInterface as Service
        interface_service = Service(self.user, self.access_token, self.request_type, self.source)
        return interface_service

    def create_users(self, member_details, source=''):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.create_users(member_details=member_details, source=source)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.add_member_details(member_details=member_details, source=source)
            return response_object

    def get_user_details_by_id(self, user_ids):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_user_details_by_id(user_ids, self.source)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.get_member_details_by_id(user_ids=user_ids, source=self.source)
            return response_object

    def get_user_details_by_usernames(self, usernames):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_user_details_by_usernames(usernames, self.source)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.get_member_details_by_usernames(usernames, self.source)
            return response_object

    def get_user_details_with_social_details(self):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_user_details_with_social_details(self.source)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.get_user_details(self.user, self.source)
            return response_object

    @handle_exceptions()
    def login_user_v2(self, auth_type=None, password=None, username=None, phone_number=None, email=None,
                      country_code=None, client_id=None, client_secret=None, scopes='read write'):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.login_user_v2(auth_type, password, username, phone_number, email,
                                                                   country_code, client_id, client_secret, scopes)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.user_login_v2(auth_type, password, username, phone_number, email,
                                                   country_code, client_id, client_secret, scopes)
            return response_object

    @handle_exceptions()
    def register_user_v2(self, reg_type=None, password=None, dob=None, gender=None, phone_number=None, email=None,
                         country_code=None, username=None, pic=None, pic_thumbnail=None, registration_source=None,
                         first_name=None, last_name=None, name=None):

        if self.request_type == 'SERVICE':
            response_object = self.interface_service.register_user_v2(reg_type, password, dob, gender, phone_number,
                                                                      email, country_code, username, pic,
                                                                      pic_thumbnail,
                                                                      registration_source, first_name, last_name, name)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.user_register_v2(reg_type, password, dob, gender, phone_number,
                                                      email, country_code, username, pic, pic_thumbnail,
                                                      registration_source, first_name, last_name, name)
            return response_object

    @handle_exceptions()
    def recover_user_password_v2(self, auth_type=None, username=None, email=None, client_id=None, client_secret=None,
                                 country_code=None, phone_number=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.recover_user_password_v2(auth_type, username, email, client_id,
                                                                              client_secret, country_code,
                                                                              phone_number)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.recover_user_password_v2(auth_type, username, email, client_id,
                                                              client_secret, country_code, phone_number)
            return response_object

    @handle_exceptions()
    def reset_user_password_v2(self, auth_type=None, username=None, email=None, password=None, token=None,
                               client_id=None,
                               client_secret=None, country_code=None,
                               phone_number=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.reset_user_password_v2(auth_type, username, email, password,
                                                                            token,
                                                                            client_id,
                                                                            client_secret, country_code, phone_number)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.reset_user_password_v2(auth_type, username, email, password, token, client_id,
                                                            client_secret, country_code, phone_number)
            return response_object

    @handle_exceptions()
    def update_user_data_with_verification(self, fields):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.update_user_data_v2(fields)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.user_data_update_with_verification(fields, self.user)
            return response_object

    @handle_exceptions()
    def verify_data_update_pre_login_v2(self, auth_type=None, email=None, country_code=None, phone_number=None,
                                        verify_token=None, client_id=None, client_secret=None, scopes='read write'):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.verify_data_update_pre_login_v2(auth_type, email, country_code,
                                                                                     phone_number, verify_token,
                                                                                     client_id, client_secret)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.verify_user_data_update_pre_login_v2(auth_type, email, country_code,
                                                                          phone_number, verify_token,
                                                                          client_id, client_secret, scopes=scopes)
            return response_object

    @handle_exceptions()
    def verify_data_update_v2(self, auth_type=None, email=None, country_code=None, phone_number=None,
                              verify_token=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.verify_data_update_v2(auth_type, email, country_code,
                                                                           phone_number,
                                                                           verify_token, self.user)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.verify_user_data_update_v2(auth_type, email, country_code, phone_number,
                                                                verify_token, self.user)
            return response_object

    @handle_exceptions()
    def activate_or_deactivate_account(self, make_active=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.activate_or_deactivate_account(make_active)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.activate_or_deactivate_account(username=self.user.username,
                                                                    make_active=make_active)
            return response_object

    @handle_exceptions()
    def social_login(self, provider=None, social_provider_token=None, social_provider_token_secret=None,
                     client_id=None,
                     client_secret=None, scopes='read write'):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.social_login(provider, social_provider_token,
                                                                  social_provider_token_secret, client_id,
                                                                  client_secret)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = UserSocialProvider.social_login(provider, social_provider_token,
                                                              social_provider_token_secret, client_id, client_secret,
                                                              scopes)
            return response_object

    @handle_exceptions()
    def user_logout(self):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.user_logout()
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.user_logout(self.user, self.access_token, source=self.source)
            return response_object

    @handle_exceptions()
    def user_logout_from_device(self, device_id, device_type):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.user_logout_from_device(device_id, device_type)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            device_info = {'device_type': device_type, 'device_id': device_id}
            response_object = IBUser.user_logout(self.user, self.access_token, device_info=device_info,
                                                 source=self.source)
            return response_object

    @handle_exceptions()
    def set_password(self, password):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.set_password(password)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.set_user_password(self.user, password)
            return response_object

    @handle_exceptions()
    def set_language(self, language):

        if self.request_type == 'SERVICE':
            response_object = self.interface_service.set_language(language)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.set_user_language(self.user.username, language)
            return response_object

    @handle_exceptions()
    def get_usp_details(self, social_ids, social_provider):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_usp_details(social_ids, social_provider)
            return response_object
        else:
            from ib_users.models.user_social_provider import UserSocialProvider
            response_object = UserSocialProvider.get_users_from_social_ids(social_ids, social_provider)
            return response_object

    def get_minimal_details(self):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_minimal_details(self.source)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.get_minimal_user_details(self.user, self.source)
            return response_object

    def get_minimal_details_by_user_ids(self, user_ids):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_minimal_details_by_user_ids(user_ids, self.source)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.get_minimal_user_details_by_user_ids(user_ids, self.source)
            return response_object

    def update_password(self, old_password, new_password):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.update_password(old_password, new_password)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.update_password(self.user, old_password, new_password)
            return response_object

    def get_users(self, user_ids, search_q, exclude_user_ids, offset=None, limit=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_users(user_ids, search_q, exclude_user_ids, self.source,
                                                               offset, limit)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.get_member_details_by_id(user_ids=user_ids, search_q=search_q,
                                                              exclude_user_ids=exclude_user_ids, source=self.source,
                                                              offset=offset, limit=limit)
            return response_object

    def validate_user_ids(self, user_ids):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.validate_user_id(user_ids)
            return response_object
        else:
            from ib_users.models.ib_user import IBUser
            response_object = IBUser.validate_user_ids(user_ids=user_ids)
            return response_object

    def validate_users_credentials_and_get_users_details(self, users_credentials):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.validate_users_credentials_and_get_user_details(
                users_credentials=users_credentials)
            return response_object
        else:
            from ib_users.utilities.validate_users_credentials_and_get_users_details \
                import validate_users_credentials_and_get_users_details
            response_object = validate_users_credentials_and_get_users_details(users_credentials=users_credentials)
            return response_object

    def link_user_social_profile(self, social_provider=None, social_token=None,
                                 social_access_token_secret=None,
                                 source=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.link_user_social_profile(
                social_provider=social_provider, social_token=social_token,
                social_access_token_secret=social_access_token_secret, source=source)
        else:
            from ib_users.models import UserSocialProvider
            response_object = UserSocialProvider.link_user_social_account(
                social_provider=social_provider, social_token=social_token,
                social_access_token_secret=social_access_token_secret, user=self.user, source=source)
        return response_object

    def get_user_detail_by_auth_type(self, auth_type=None, email=None, phone_number=None, country_code=None,
                                     username=None, source=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_user_detail_by_auth_type(auth_type=auth_type, email=email,
                                                                                  phone_number=phone_number,
                                                                                  country_code=country_code,
                                                                                  username=username, source=source)
        else:
            from ib_users.models import IBUser
            response_object = IBUser.get_user_by_auth_type(auth_type=auth_type, email=email,
                                                           phone_number=phone_number,
                                                           country_code=country_code,
                                                           username=username, source=source)

        return response_object

    def check_username_availability(self, username=None, source=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.check_username_availability(username=username, source=source)
        else:
            from ib_users.models import IBUser
            response_object = IBUser.check_username_availability(username=username)

        return response_object

    @handle_exceptions()
    def get_user(self, source=''):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.get_user(source=source)
        else:
            from ib_users.models import IBUser
            response_object = IBUser.get_user_details(user=self.user, source=source)

        return response_object

    def delink_user_social_profile(self, social_provider=None, source=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.delink_user_social_account(
                social_provider=social_provider, source=source)
        else:
            from ib_users.models import UserSocialProvider
            response_object = UserSocialProvider.de_link_user_social_account(
                social_provider=social_provider, user=self.user, source=source)
        return response_object

    @handle_exceptions()
    def update_user_details(self, user_details=None, source=''):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.update_user_details(user_details=user_details, source=source)
        else:
            from ib_users.models import IBUser
            response_object = IBUser.update_user_details(user=self.user, user_details=user_details, source=source)
        return response_object

    def search_user_by_auth_type(self, auth_type=None, username=None, phone_number=None, email=None,
                                 country_code=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.search_user_by_auth_type(auth_type, username, phone_number, email,
                                                                              country_code)
        else:
            from ib_users.models import IBUser
            response_object = IBUser.search_user_by_auth_type(auth_type, username, phone_number, email, country_code,
                                                              self.source)
        return response_object

    @handle_exceptions()
    def resend_otp_v2_for_data_verification(self, auth_type=None, phone_number=None, email=None, country_code=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.resend_otp_v2_for_data_verification(auth_type=auth_type,
                                                                                         phone_number=phone_number,
                                                                                         email=email,
                                                                                         country_code=country_code)
        else:
            from ib_users.models import IBUser
            response_object = IBUser.resend_otp_v2_for_data_verification(self.user, auth_type=auth_type,
                                                                         phone_number=phone_number, email=email,
                                                                         country_code=country_code)
        return response_object

    @handle_exceptions()
    def user_login_v2_with_otp(self, auth_type=None, phone_number=None, email=None, country_code=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.user_login_v2_with_otp(auth_type=auth_type,
                                                                            phone_number=phone_number, email=email,
                                                                            country_code=country_code)
        else:
            from ib_users.models import IBUser
            response_object = IBUser.user_login_v2_with_otp(auth_type=auth_type, phone_number=phone_number,
                                                            email=email, country_code=country_code)
        return response_object

    @handle_exceptions()
    def user_login_v2_verify_otp(self, auth_type=None, phone_number=None, email=None, country_code=None,
                                 client_secret=None, client_id=None,
                                 verify_token=None, scopes='read write update delete'):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.user_login_v2_verify_otp(auth_type=auth_type,
                                                                              phone_number=phone_number,
                                                                              email=email, country_code=country_code,
                                                                              client_id=client_id,
                                                                              client_secret=client_secret,
                                                                              verify_token=verify_token, scopes=scopes)
        else:
            from ib_users.models import IBUser
            response_object = IBUser.user_login_v2_verify_otp(auth_type=auth_type, phone_number=phone_number,
                                                              email=email, country_code=country_code,
                                                              client_id=client_id, client_secret=client_secret,
                                                              verify_token=verify_token, scopes=scopes)
        return response_object

    @handle_exceptions()
    def resend_otp_v2_for_verified_auth(self, auth_type=None, phone_number=None, email=None, country_code=None):
        if self.request_type == 'SERVICE':
            response_object = self.interface_service.resend_otp_v2_for_verified_auth(auth_type=auth_type,
                                                                                     phone_number=phone_number,
                                                                                     email=email,
                                                                                     country_code=country_code)
        else:
            from ib_users.models import IBUser
            response_object = IBUser.resend_otp_v2_for_verified_auth(auth_type=auth_type, phone_number=phone_number,
                                                                     email=email, country_code=country_code)
        return response_object

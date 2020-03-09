from django.db import models
from django.db.models.query_utils import Q
from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_users.constants.social_providers import SocialProviders
from ib_users.models.ib_user import IBUser
from ib_users.models.social_provider import SocialProvider
from ib_users.models.user_otp import UserOTP
from ib_users.utilities.generate_random_username import generate_user_name
from ib_users.utilities.get_oauth_details_response import get_oauth_details_response

__author__ = 'tanmay.ibhubs'


class UserSocialProviderManager(models.Manager):
    def get_queryset(self):
        return super(UserSocialProviderManager, self).get_queryset().filter(is_deleted=False)


class UserSocialProvider(AbstractDateTimeModel):
    ib_user = models.ForeignKey('ib_users.IBUser', related_name='ib_user_key')
    social_provider = models.ForeignKey('ib_users.SocialProvider', related_name='social_provider_key')
    social_token = models.CharField(max_length=500, default='')
    social_id = models.CharField(max_length=100, default='')
    social_name = models.CharField(max_length=50, default='')
    extra_info = models.CharField(max_length=500, default='', null=True)
    is_deleted = models.BooleanField(default=False, null=False)

    class Meta:
        verbose_name = "User Social Provider"
        app_label = 'ib_users'

    objects = UserSocialProviderManager()

    def __unicode__(self):
        return str(self.ib_user) + "/" + str(self.social_provider)

    def convert_to_dict(self):
        return {
            'user_id': self.ib_user.id,
            'social_provider': self.social_provider.name,
            'social_id': self.social_id,
            'social_name': self.social_name
        }

    @classmethod
    def convert_to_dict_without_user_from_dict(cls, provider_dict):
        return {
            'social_provider': provider_dict["social_provider__name"],
            'social_id': provider_dict["social_id"],
            'social_name': provider_dict["social_name"],
        }


    @classmethod
    def social_login(cls, provider=None, social_provider_token=None, social_provider_token_secret=None, client_id=None,
                     client_secret=None, scopes='read write'):
        response_object = {}
        try:
            from ib_users.utilities.social_login_utility import get_details_from_facebook, get_details_from_google, \
                get_details_from_twitter, get_details_from_linkedin
            if provider == SocialProviders.FACEBOOK.value:
                response_object = get_details_from_facebook(social_provider_token)

                email = response_object.get('email', None)
                if not email:
                    raise BadRequest('Email scope is not provided.', res_status=False)

                user = IBUser.objects.get(email=response_object['email'])

            elif provider == SocialProviders.GOOGLE.value:
                response_object = get_details_from_google(social_provider_token)
                print "------->", response_object
                email = response_object.get('email', None)
                if not email:
                    raise BadRequest('Email scope is not provided.', res_status=False)

                user = IBUser.objects.get(email=response_object['email'])
                print user

            elif provider == SocialProviders.TWITTER.value:
                response_object = get_details_from_twitter(social_provider_token, social_provider_token_secret)
                email = response_object.get('email', None)
                if not email:
                    raise BadRequest('Email scope is not provided.', res_status=False)

                user = IBUser.objects.get(email=response_object['email'])


            elif provider == SocialProviders.LINKEDIN.value:
                response_object = get_details_from_linkedin(social_provider_token)
                email = response_object.get('email', None)
                if not email:
                    raise BadRequest('Email scope is not provided.', res_status=False)

                user = IBUser.objects.get(Q(phone_number=response_object['phone_number']) & Q(
                    country_code=response_object['country_code']) |
                                          Q(email=response_object['email']))

                if user.phone_number != response_object['phone_number']:
                    user.phone_number = response_object['phone_number']
                    user.country_code = response_object['country_code']
                    user.save()
                    UserOTP.send_otp(user, 'phone_number')

                elif user.email != response_object['email']:
                    user.email = response_object['email']
                    user.save()
                    UserOTP.send_otp(user, 'email')

            else:
                raise BadRequest('Social Provider -> facebook|twitter|google', res_status='failed')


        except IBUser.DoesNotExist:
            user = IBUser(username=generate_user_name(username=response_object['name']))
            user.email = response_object.get('email', None)
            user.phone_number = response_object.get('phone_number', None)
            user.country_code = response_object.get('country_code', None)
            user.name = response_object.get('name', '')
            user.is_phone_verified = True
            user.is_email_verified = True
            user.save()

        social_provider, is_created = SocialProvider.objects.get_or_create(name=provider)
        usp, is_created = cls.objects.get_or_create(ib_user=user, social_provider=social_provider)

        if not is_created:
            usp.is_deleted = True
            usp.save()
            usp, is_created = cls.objects.get_or_create(ib_user=user, social_provider=social_provider)

        if social_provider.name == SocialProviders.TWITTER.value:
            usp.social_token = social_provider_token
            usp.extra_info = social_provider_token_secret
        else:
            usp.social_token = social_provider_token

        usp.social_id = str(response_object['id'])
        usp.social_name = response_object['name']
        usp.extra_info = social_provider_token_secret
        usp.save()
        return get_oauth_details_response(user, client_id, client_secret, scopes)

    @classmethod
    def get_users_from_social_ids(cls, social_ids, social_provider):
        try:
            social_provider = SocialProvider.objects.get(name=social_provider)
        except:
            raise BadRequest('SocialProvider not found', res_status='failed')
        print social_provider
        users = cls.objects.filter(social_id__in=social_ids, social_provider=social_provider)
        print users
        return cls.get_minimal_user_detail(users)

    @classmethod
    def link_user_social_account(cls, social_provider=None, social_token=None,
                                 social_access_token_secret=None,
                                 user=None, **kwargs):

        from ib_users.utilities.social_login_utility import get_details_from_facebook, get_details_from_google, \
            get_details_from_twitter, get_details_from_linkedin
        if social_provider == SocialProviders.FACEBOOK.value:
            response_object = get_details_from_facebook(social_token)

        elif social_provider == SocialProviders.GOOGLE.value:
            response_object = get_details_from_google(social_token)

        elif social_provider == SocialProviders.TWITTER.value:
            response_object = get_details_from_twitter(social_token, social_access_token_secret)

        elif social_provider == SocialProviders.LINKEDIN.value:
            response_object = get_details_from_linkedin(social_token)

        else:
            from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
            raise BadRequest('Social Provider -> facebook|twitter|google', res_status='failed')

        if 'id' not in response_object:
            from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
            raise BadRequest('User detail can\'t be fetched.', res_status=False)

        social_provider, is_created = SocialProvider.objects.get_or_create(name=social_provider)

        usp, is_created = cls.objects.get_or_create(ib_user=user, social_provider=social_provider)

        if not is_created:
            usp.is_deleted = True
            usp.save()
            usp, is_created = cls.objects.get_or_create(ib_user=user, social_provider=social_provider)

        if social_provider.name == SocialProviders.TWITTER.value:
            usp.social_token = social_token
            usp.extra_info = social_access_token_secret
        else:
            usp.social_token = social_token

        usp.social_id = response_object['id']
        usp.social_name = response_object.get('name', None)
        usp.save()
        return {
            "social_provider": usp.social_provider,
            "user_id": user.id,
            "social_id": usp.social_id,
            "social_name": usp.social_name
        }

    @staticmethod
    def get_minimal_user_detail(usp_details):
        usp_dict_list = []
        for usp in usp_details:
            usp_dict = {
                'user_id': usp.ib_user.id,
                'social_id': usp.social_id,
                'social_name': usp.social_name
            }
            usp_dict_list.append((usp_dict))
        return usp_dict_list

    @classmethod
    def de_link_user_social_account(cls, social_provider=None,
                                    user=None, **kwargs):
        try:
            usp = cls.objects.filter(ib_user=user, social_provider=social_provider).latest('creation_datetime')
        except:
            from django_swagger_utils.drf_server.exceptions.not_found import NotFound
            raise NotFound('User hasn\'t linked his account', res_status=False)
        cls.objects.filter(ib_user=user, social_provider=social_provider).update(is_deleted=True)
        return usp.convert_to_dict()

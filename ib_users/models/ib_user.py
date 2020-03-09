from collections import defaultdict
from datetime import datetime

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
from django_swagger_utils.drf_server.exceptions.forbidden import Forbidden
from django_swagger_utils.drf_server.exceptions.not_found import NotFound
from django_swagger_utils.drf_server.exceptions.unauthorized import \
    Unauthorized
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel
from oauth2_provider.models import AccessToken, RefreshToken

from ib_users.constants.user_reg_type import UserRegistrationType
from ib_users.models.change_history import ChangeHistory
from ib_users.models.ib_user_registration_source import \
    IBUserRegistrationSource
from ib_users.models.registration_source import RegistrationSource
from ib_users.utilities.generate_random_username import generate_user_name
from ib_users.utilities.get_oauth_details_response import \
    get_oauth_details_response


class IBUserManager(UserManager):
    def get_queryset(self):
        return super(IBUserManager, self).get_queryset().filter(
            is_deleted=False)


class IBUser(AbstractUser, AbstractDateTimeModel):
    from ib_common.constants.language_choices import LANGUAGE_CHOICES, \
        DEFAULT_LANGUAGE
    language = models.CharField(max_length=100, default=DEFAULT_LANGUAGE,
                                choices=LANGUAGE_CHOICES, null=True)
    pic = models.CharField(max_length=500, blank=True, null=True)
    pic_thumbnail = models.CharField(max_length=500, blank=True, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True,
                              null=True)
    dob = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True)
    registration_sources = models.ManyToManyField(
        'ib_users.RegistrationSource',
        through='ib_users.IBUserRegistrationSource')
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    change_history = models.ManyToManyField('ib_users.ChangeHistory')
    is_deleted = models.BooleanField(null=False, default=False)
    social_provider = models.ManyToManyField('ib_users.SocialProvider',
                                             through='ib_users.UserSocialProvider',
                                             related_name='social_provider_user')

    objects = IBUserManager()
    all_objects = UserManager()

    class Meta:
        verbose_name = "IB User"
        app_label = 'ib_users'

    @property
    def event_id(self):
        return 'USER_ID-' + str(self.id)

    def __unicode__(self):
        return str(self.id)

    def convert_to_dict(self):
        return {"m_username": self.username, "m_id": self.id,
                "m_status": self.status,
                "dob": self.dob, 'm_phone_number': self.phone_number,
                'm_email': self.email}

    @classmethod
    def get_user_details(cls, user, source):
        user_details_all = cls.objects.get(username=user.username).__dict__
        user_details = dict()
        fields = ['id', 'username', 'name', 'gender', 'pic', 'pic_thumbnail',
                  'first_name', 'last_name',
                  'phone_number', 'email', 'country_code', 'language', 'dob',
                  'is_staff']
        for field in fields:
            if field == 'dob':
                user_details[field] = user_details_all[field]
            else:
                user_details['m_' + field] = user_details_all[field]
        user_details['is_admin'] = user_details_all['is_staff']
        user_details['is_active'] = user_details_all['is_active']
        from ib_users.models import UserExtraData
        user_details['extra_details'] = UserExtraData.get_extra_data_for_user(
            user, source)

        from ib_users.models import UserSocialProvider
        social_details = UserSocialProvider.objects.filter(ib_user__id=user.id) \
            .values('social_provider__name', 'social_id', 'social_name')
        social_details_list = [
            UserSocialProvider.convert_to_dict_without_user_from_dict(
                social_detail) for
            social_detail in social_details]
        user_details['social_details'] = social_details_list
        return user_details

    @classmethod
    def get_minimal_user_details(cls, user, source):
        user_details_all = cls.objects.get(username=user.username)

        user_details = {
            'm_id': user_details_all.id,
            'm_username': user_details_all.username,
            'm_name': user_details_all.name,
            'm_pic': user_details_all.pic,
            'm_pic_thumbnail': user_details_all.pic_thumbnail

        }
        return user_details

    @classmethod
    def get_user_by_auth_type(cls, auth_type=None, email=None,
                              phone_number=None, country_code=None,
                              username=None,
                              **kwargs):
        try:
            if auth_type == UserRegistrationType.EMAIL.value and email is not None:
                user = IBUser.objects.get(email=email)

            elif auth_type == UserRegistrationType.USERNAME.value and username is not None:
                user = IBUser.objects.get(username=username)

            elif auth_type == UserRegistrationType.PHONE_NUMBER.value and phone_number is not None:
                user = IBUser.objects.get(phone_number=phone_number,
                                          country_code=country_code)

            else:
                raise BadRequest(str(_('\'auth_type\' is not correct.')),
                                 res_status='')

            user_details = {
                'm_id': user.id,
                'm_username': user.username,
                'm_name': user.name,
                'm_pic': user.pic,
                'm_pic_thumbnail': user.pic_thumbnail

            }

            return user_details
        except IBUser.DoesNotExist:
            from django_swagger_utils.drf_server.exceptions.not_found import \
                NotFound
            raise NotFound(str(_('User not found')), res_status='')

    @classmethod
    def get_minimal_user_details_by_user_ids(cls, user_ids, source):
        users = cls.objects.filter(id__in=user_ids)
        users_details_list = []
        for user in users:
            user_details = {
                'm_id': user.id,
                'm_username': user.username,
                'm_name': user.name,
                'm_pic': user.pic,
                'm_pic_thumbnail': user.pic_thumbnail

            }
            users_details_list.append(user_details)
        return users_details_list

    @classmethod
    def update_user_details(cls, user, user_details, source):
        not_allowed_list = ["email", "username", "phone_number",
                            "country_code"]
        fields = IBUser._meta
        from django.conf import settings

        # IB_USERS_CHANGE_ALLOWED_AUTH_TYPES = ['email']
        change_allowed_auth_types_without_verification = getattr(
            settings,
            'IB_USERS_CHANGE_ALLOWED_AUTH_TYPES',
            []
        )

        for user_detail in user_details:
            key = user_detail['ud_key']
            value = user_detail['ud_value']

            if key in not_allowed_list and key not in \
                    change_allowed_auth_types_without_verification:
                continue

            if key == 'email' and getattr(user, key) != value:
                setattr(user, 'is_email_verified', False)

            if key == 'phone_number' and getattr(user, key) != value:
                setattr(user, 'is_phone_verified', False)

            if key == 'country_code' and getattr(user, key) != value:
                setattr(user, 'is_phone_verified', False)

            try:
                fields.get_field(key)
                setattr(user, key, value)
            except:
                from ib_users.models import UserExtraData
                UserExtraData.add_key_value_pair(user, key, value, source)
        user.save()
        return {"res_status": "200 OK, status=200"}

    @classmethod
    def get_member_details_by_usernames(cls, usernames, source):
        ib_users = IBUser.objects.filter(username__in=usernames)
        return IBUser.get_member_details(ib_users, source)

    @classmethod
    def get_member_details_by_id(cls, user_ids, search_q=None,
                                 exclude_user_ids=None, source=None,
                                 offset=None,
                                 limit=None):

        if exclude_user_ids is None:
            exclude_user_ids = []

        ib_users = IBUser.objects.all()
        if exclude_user_ids:
            ib_users = ib_users.exclude(id__in=exclude_user_ids)
        if user_ids:
            ib_users = ib_users.filter(id__in=user_ids)
        if search_q:
            from django.db.models import Q
            ib_users = ib_users.filter(
                Q(username__icontains=search_q) |
                Q(name__icontains=search_q)
            )
        total = ib_users.count()

        if not limit or limit == -1:
            limit = total

        if not offset:
            offset = 0

        # ib_users = ib_users[offset:offset + limit]
        response_list = IBUser.get_member_details(ib_users, source)
        response_list = response_list[offset:offset + limit]
        return response_list

    @classmethod
    def search_user_by_auth_type(cls, auth_type=None, username=None,
                                 phone_number=None, email=None,
                                 country_code=None,
                                 source=None):
        if auth_type == UserRegistrationType.EMAIL.value and email is not None and email.strip() != '':
            users = IBUser.objects.filter(email=email)
        elif auth_type == UserRegistrationType.USERNAME.value and username is not None and username.strip() != '':
            users = IBUser.objects.filter(username=username)
        elif auth_type == UserRegistrationType.PHONE_NUMBER.value and phone_number is not None and phone_number.strip() != '':
            users = IBUser.objects.filter(phone_number=phone_number,
                                          country_code=country_code)
        else:
            users = []
        response_list = IBUser.get_member_details(users, source, get_article = None)
        return response_list

    @staticmethod
    def get_member_details_dict_from_obj(ib_user):
        data = {"m_username": ib_user.username, "m_id": ib_user.id,
                "m_pic": ib_user.pic, "m_name": ib_user.name,
                "m_pic_thumbnail": ib_user.pic_thumbnail,
                "m_status": ib_user.status, 'dob': ib_user.dob,
                "m_gender": ib_user.gender, "m_email": ib_user.email,
                "m_phone_number": ib_user.phone_number,
                "m_country_code": ib_user.country_code,
                "first_name": ib_user.first_name,
                "last_name": ib_user.last_name,
                "is_phone_verified": ib_user.is_phone_verified,
                "is_email_verified": ib_user.is_email_verified,
                "is_staff": ib_user.is_staff}
        return data


    @classmethod
    def get_member_details(cls, ib_users, source):
        response_list = list()
        user_extra_data = cls.get_user_extra_data_id_dict(ib_users, source)

        for ib_user in ib_users:
            user_dict = cls.get_member_details_dict_from_obj(ib_user)
            user_dict['extra_details'] = user_extra_data.get(
                ib_user.id) if user_extra_data.get(ib_user.id) else []
            response_list.append(user_dict)
        return response_list

    @classmethod
    def get_user_extra_data_id_dict(cls, users, source):
        from ib_users.models import UserExtraData
        user_extra_data_objs = UserExtraData.objects.filter(ib_user__in=users,
                                                            source=source)
        user_extra_data = defaultdict(list)
        for extra_data_obj in user_extra_data_objs:
            user_extra_data[extra_data_obj.ib_user_id].append(
                extra_data_obj.convert_to_ud_dict())
        return user_extra_data

    @classmethod
    def get_user_language(cls, member_id):
        try:
            language = IBUser.objects.get(id=member_id).language
            res_status = "Success"
        except IBUser:
            language = str()
            res_status = "Invalid member_id"

        return {"language": language, "res_status": res_status}

    @staticmethod
    def validate_user_ids(user_ids):
        invalid_user_ids = list()
        ib_user_objs = IBUser.objects.filter(id__in=user_ids)
        for each_obj in ib_user_objs:
            if each_obj.id not in user_ids:
                invalid_user_ids.append(each_obj.id)
        return {'invalid_user_ids': invalid_user_ids}

    @staticmethod
    def update_password(user, old_password, new_password):
        is_valid = user.check_password(old_password)
        if not is_valid:
            raise Forbidden(str(_('Incorrect password! Try again.')),
                            res_status='')
        ChangeHistory.create_change_history(user.id, old_password,
                                            new_password, True, 'session')
        user.set_password(new_password)
        user.save()
        return

    @staticmethod
    def set_user_password(user, new_password):
        ChangeHistory.create_change_history(user.id, '', new_password, True,
                                            'session')
        user.set_password(new_password)
        user.save()
        return

    @staticmethod
    def get_user_id_from_username(username, password):
        try:
            ib_user = IBUser.objects.get(username=username)
            if ib_user.check_password(password) is True:
                return {'res_status': "Success", "user_id": ib_user.id}
            else:
                return {'res_status': "Incorrect Password", "user_id": -1}
        except IBUser.DoesNotExist:
            return {'res_status': "Please enter valid credentials",
                    "user_id": -1}

    @classmethod
    def register_user_by_phone_number(cls, phone_number, country_code):
        try:
            user = IBUser.objects.get(
                phone_number=phone_number,
                country_code=country_code
            )
            if user.is_phone_verified:
                raise BadRequest(str(_('Phone number already registered')),
                                 res_status='')

            user.phone_number = ''
            user.save()

            new_phone_number = country_code + "," + phone_number
            ChangeHistory.create_change_history(
                user.id, '', new_phone_number, False,
                UserRegistrationType.PHONE_NUMBER.value)

        except IBUser.DoesNotExist:
            pass

    @classmethod
    def register_user_by_email(cls, email):
        try:
            user = IBUser.objects.get(email=email)
            if user.is_email_verified:
                raise BadRequest(str(_('Email already registered')),
                                 res_status='')

            user.email = ''
            user.save()

            ChangeHistory.create_change_history(
                user.id, '', user.email, False,
                UserRegistrationType.EMAIL.value)

        except IBUser.DoesNotExist:
            pass

    @classmethod
    def user_register_v2(cls, reg_type=None, password=None, dob=None,
                         gender=None, phone_number=None, email=None,
                         country_code=None, username=None, pic=None,
                         pic_thumbnail=None, registration_source=None,
                         first_name='', last_name='', name=''):

        if username == '' or username is None:
            username = generate_user_name(username=None)
        try:
            user_by_username = IBUser.objects.get(username=username)
            raise BadRequest(str(_('Username already exist.')), res_status='')
        except IBUser.DoesNotExist:
            pass

        if reg_type == UserRegistrationType.EMAIL.value and email is not None:
            cls.register_user_by_email(email)

        elif reg_type == UserRegistrationType.PHONE_NUMBER.value \
                and phone_number is not None:
            cls.register_user_by_phone_number(phone_number, country_code)

        elif reg_type == UserRegistrationType.EMAIL_AND_PHONE_NUMBER.value \
                and email is not None and phone_number is not None:
            cls.register_user_by_email(email)
            cls.register_user_by_phone_number(phone_number, country_code)

        elif reg_type == UserRegistrationType.USERNAME.value and username is not None:
            pass

        else:
            raise BadRequest(str(_('\'reg_type\' is not correct.'
                                   )), res_status='')

        if last_name is None:
            last_name = ''
        if first_name is None:
            first_name = ''

        user = IBUser(username=username)
        user.name = name
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.country_code = country_code
        user.email = email
        user.username = username
        user.set_password(password)
        if dob == '':
            dob = None
        user.dob = dob
        user.gender = gender
        user.pic = pic
        user.pic_thumbnail = pic_thumbnail
        user.save()

        registration_source_obj, is_created = RegistrationSource.objects \
            .get_or_create(registration_source=registration_source)
        IBUserRegistrationSource.create_user_registration_source(
            user,
            registration_source_obj
        )
        from ib_users.models.user_otp import UserOTP
        UserOTP.send_otp(user, reg_type)

        callback_dict = {
            'auth_type': reg_type,
            'username': username,
            'phone_number': phone_number,
            'country_code': country_code,
            'email': email,
            'm_id': user.id,
            'user_id': user.id,
            'm_username': user.username,
            'm_name': user.name,
            'm_pic': user.pic,
            'm_pic_thumbnail': user.pic_thumbnail
        }

        cls.signal_for_new_user_registered_evaluate(
            user_callback_dict=callback_dict)
        return {'username': user.username, 'user_id': user.id}

    @classmethod
    def user_login_v2(cls, auth_type=None, password=None, username=None,
                      phone_number=None, email=None,
                      country_code=None, client_id=None, client_secret=None,
                      scopes='read write update delete',
                      source=''):
        if auth_type == UserRegistrationType.EMAIL.value and email is not None:
            try:
                user = IBUser.objects.get(email=email)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The email address that you\'ve entered doesn\'t match any account.')),
                    res_status='')
            if not user.is_email_verified:
                raise Unauthorized(str(_('Email verification is pending.')),
                                   res_status='')
        elif auth_type == UserRegistrationType.USERNAME.value and username is not None:
            try:
                user = IBUser.objects.get(username=username)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The username that you\'ve entered doesn\'t match any account.')),
                    res_status='')
        elif auth_type == UserRegistrationType.PHONE_NUMBER.value and phone_number is not None:
            try:
                user = IBUser.objects.get(phone_number=phone_number,
                                          country_code=country_code)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The phone number that you\'ve entered doesn\'t match any account.')),
                    res_status='')
            if not user.is_phone_verified:
                raise Unauthorized(
                    str(_('Phone number verification is pending')),
                    res_status='')
        else:
            raise BadRequest(str(_('\'auth_type\' is not correct.'
                                   )), res_status='')

        is_valid = user.check_password(password)
        if not is_valid:
            raise Forbidden(str(_('Incorrect password! Try again.')),
                            res_status='')

        emit_user_activated_signal = False
        if not user.is_active:
            emit_user_activated_signal = True
            user.is_active = True
            user.save()
        response = get_oauth_details_response(user, client_id, client_secret,
                                              scopes)
        access_token = response['tokens'].get('access_token')
        if emit_user_activated_signal and access_token:
            cls.signal_for_user_activated_evaluate({'m_id': user.id}, user,
                                                   source=source,
                                                   access_token=access_token)

        return response

    @classmethod
    def reset_user_password_v2(cls, auth_type=None, username=None, email=None,
                               password=None, token=None,
                               client_id=None,
                               client_secret=None, country_code=None,
                               phone_number=None):
        if auth_type == UserRegistrationType.EMAIL.value and email is not None:
            if not email:
                raise BadRequest(str(_('Your email address can\'t be empty')))
            try:
                user = IBUser.objects.get(email=email,
                                          is_email_verified=True)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The email address that you\'ve entered doesn\'t match any account.')),
                    res_status='')
        elif auth_type == UserRegistrationType.USERNAME.value and username is not None:
            if not username:
                raise BadRequest(str(_('Your username can\'t be empty')))
            try:
                user = IBUser.objects.get(username=username)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The username that you\'ve entered doesn\'t match any account.')),
                    res_status='')
        elif auth_type == UserRegistrationType.PHONE_NUMBER.value and phone_number is not None:
            if not phone_number:
                raise BadRequest(str(_('Your phone number can\'t be empty')))
            try:
                user = IBUser.objects.get(phone_number=phone_number,
                                          country_code=country_code,
                                          is_phone_verified=True)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The phone number that you\'ve entered doesn\'t match any account.')),
                    res_status='')

        else:
            raise BadRequest(str(_('\'auth_type\' is not correct.'
                                   )), res_status='')
        from ib_users.models.user_otp import UserOTP
        is_validated = UserOTP.validate_otp(user, token, auth_type)

        if not is_validated:
            raise Forbidden(str(_('Invalid OTP')), res_status='')

        old_password = user.password
        user.set_password(password)
        ChangeHistory.create_change_history(user.id, old_password,
                                            user.password, True, 'password')

        user.save()
        return {"success": True}

    @classmethod
    def recover_user_password_v2(cls, auth_type=None, username=None,
                                 email=None, client_id=None,
                                 client_secret=None,
                                 country_code=None, phone_number=None):
        if auth_type == UserRegistrationType.EMAIL.value and email is not None:
            try:
                user = IBUser.objects.get(email=email, is_email_verified=True)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The email address that you\'ve entered doesn\'t match any account.')),
                    res_status='')
        elif auth_type == UserRegistrationType.USERNAME.value and username is not None:
            try:
                user = IBUser.objects.get(username=username)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The username that you\'ve entered doesn\'t match any account.')),
                    res_status='')
            auth_type = UserRegistrationType.EMAIL_AND_PHONE_NUMBER.value
        elif auth_type == UserRegistrationType.PHONE_NUMBER.value and phone_number is not None:
            try:
                user = IBUser.objects.get(phone_number=phone_number,
                                          country_code=country_code,
                                          is_phone_verified=True)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The phone number that you\'ve entered doesn\'t match any account.')),
                    res_status='')
        else:
            raise BadRequest(str(_('\'auth_type\' is not correct.'
                                   )), res_status='')

        from ib_users.models.user_otp import UserOTP
        UserOTP.send_otp(user, auth_type)

        return {"success": True}

    @classmethod
    def user_data_update_with_verification(cls, fields=None, user=None):
        for field in fields:
            if 'update_type' not in field:
                raise BadRequest(str(_('\'update_type\' not found')),
                                 res_status='')
            if field[
                'update_type'] == UserRegistrationType.EMAIL.value and 'email' in field:

                if user.email == field['email']:
                    raise BadRequest(str(_('Email not changed')),
                                     res_status='')
                # skip the update data if data not changed

                try:
                    cls.get_user_by_auth_type(
                        auth_type=UserRegistrationType.EMAIL.value,
                        email=field['email'])
                    raise BadRequest(str(_('Verified email already exists')),
                                     res_status='')
                except NotFound:

                    # deleting old change history records to ensure allow only
                    # one change of record for each change type
                    ChangeHistory.objects.filter(
                        user_id=user.id,
                        old_val=user.email,
                        is_verified=False,
                        type=field['update_type']
                    ).update(is_deleted=True)

                    # deleting the non verified new phone number request from
                    # all users
                    ChangeHistory.objects.filter(
                        new_val=field['email'],
                        is_verified=False,
                        type=field['update_type']
                    ).update(is_deleted=True)

                    ChangeHistory.create_change_history(user.id, user.email,
                                                        field['email'], False,
                                                        field['update_type'])
                    from ib_users.models.user_otp import UserOTP
                    UserOTP.send_otp(user, field['update_type'],
                                     email=field['email'])
            elif field[
                'update_type'] == UserRegistrationType.USERNAME.value and 'username' in field:
                pass
            elif field[
                'update_type'] == UserRegistrationType.PHONE_NUMBER.value and 'phone_number' in field:

                if user.phone_number == field['phone_number'] and \
                                user.country_code == field['country_code']:
                    raise BadRequest(str(_('Phone number not changed')),
                                     res_status='')
                # skip the update data if data not changed

                try:
                    cls.get_user_by_auth_type(
                        auth_type=UserRegistrationType.PHONE_NUMBER.value,
                        country_code=field['country_code'],
                        phone_number=field['phone_number'])
                    raise BadRequest(
                        str(_('Verified phone number already exists')))
                except NotFound:
                    print getattr(user, 'country_code', '')
                    print getattr(user, 'phone_number', '')

                    user.phone_number = user.phone_number if \
                        user.phone_number is not None else ''
                    user.country_code = user.country_code if \
                        user.country_code is not None else ''

                    old_complete_phone_number = \
                        getattr(user, 'country_code', '') + "," + \
                        getattr(user, 'phone_number', '')

                    new_phone_number = field['country_code'] + "," + field[
                        "phone_number"]

                    # deleting old change history records to ensure allow only
                    # one change of record for each change type
                    print ChangeHistory.objects.filter(
                        user_id=user.id,
                        old_val=old_complete_phone_number,
                        is_verified=False,
                        type=field['update_type']
                    ).update(is_deleted=True)

                    # deleting the non verified new phone number request from
                    # all users
                    ChangeHistory.objects.filter(
                        new_val=new_phone_number,
                        is_verified=False,
                        type=field['update_type']
                    ).update(is_deleted=True)

                    print ChangeHistory.create_change_history(user.id,
                                                              old_complete_phone_number,
                                                              new_phone_number,
                                                              False,
                                                              field[
                                                                  'update_type'])
                    from ib_users.models.user_otp import UserOTP
                    UserOTP.send_otp(user, field['update_type'],
                                     phone_number=field["phone_number"],
                                     country_code=field["country_code"])
            else:
                raise BadRequest(str(_('\'update_type\' is not correct.'
                                       )), res_status='')

        return {"success": True}

    @classmethod
    def remove_linked_email_or_phone_number(cls, email=None, phone_number=None,
                                            country_code=None):
        try:
            if email is not None:
                user = IBUser.objects.get(email=email)
                user.email = ''
                user.is_email_verified = False
                user.save()

            if phone_number is not None:
                user = IBUser.objects.get(
                    phone_number=phone_number,
                    country_code=country_code)
                user.phone_number = ''
                user.is_phone_verified = False
                user.save()

        except:
            pass

    @classmethod
    def add_member_details(cls, member_details, source=''):
        response_list = list()
        for member_detail in member_details:
            from ib_users.utilities.create_user_and_get_member_id import \
                create_user_and_get_member_id
            if 'dob' in member_detail.keys() and member_detail['dob'] != "":
                from datetime import datetime
                dob = member_detail['dob']
                dob = datetime.strptime(dob, '%Y-%m-%d')
            else:
                dob = None
            ib_user_obj = create_user_and_get_member_id(source,
                                                        member_detail[
                                                            'username'],
                                                        member_detail['name'],
                                                        member_detail['pic'],
                                                        dob)

            response_list.append(
                {"m_username": ib_user_obj.username, "m_id": ib_user_obj.id,
                 "m_pic": ib_user_obj.pic,
                 "m_name": ib_user_obj.name, "m_status": ib_user_obj.status,
                 "m_pic_thumbnail": ib_user_obj.pic_thumbnail,
                 "dob": ib_user_obj.dob,
                 "is_admin": member_detail['is_admin']})
        return response_list

    @classmethod
    def verify_user_data_update_v2(cls, auth_type=None, email=None,
                                   country_code=None, phone_number=None,
                                   verify_token=None, user=None):
        if auth_type == UserRegistrationType.EMAIL.value and email is not None:
            from ib_users.models.user_otp import UserOTP
            is_validated = UserOTP.validate_otp(user, verify_token, auth_type)
            if not is_validated:
                raise BadRequest(str(_('Invalid OTP')), res_status='')

            try:
                change_history = ChangeHistory.objects.get(user_id=user.id,
                                                           old_val=user.email,
                                                           new_val=email,
                                                           is_verified=False)
                change_history.is_verified = True
                change_history.save()
            except ChangeHistory.DoesNotExist:
                raise BadRequest(str(_('Invalid OTP Verification')),
                                 res_status='')

            cls.remove_linked_email_or_phone_number(email=email)
            user.email = email
            user.is_email_verified = True
            user.save()

        elif auth_type == UserRegistrationType.PHONE_NUMBER.value and phone_number is not None:
            from ib_users.models.user_otp import UserOTP
            is_validated = UserOTP.validate_otp(user, verify_token, auth_type)
            if not is_validated:
                raise Forbidden(str(_('Invalid OTP')), res_status='')

            old_complete_phone_number = user.country_code + "," + user.phone_number
            new_phone_number = country_code + "," + phone_number
            try:
                change_history = ChangeHistory.objects.get(user_id=user.id,
                                                           old_val=old_complete_phone_number,
                                                           new_val=new_phone_number,
                                                           is_verified=False)
                change_history.is_verified = True
                change_history.save()
            except ChangeHistory.DoesNotExist:
                raise BadRequest(str(_('Invalid OTP Verification')),
                                 res_status='')

            cls.remove_linked_email_or_phone_number(
                phone_number=phone_number,
                country_code=country_code
            )
            user.country_code = country_code
            user.phone_number = phone_number
            user.is_phone_verified = True
            user.save()

        else:
            raise BadRequest(str(_('\'auth_type\' is not correct.')))

        return {"success": True}

    @classmethod
    def verify_user_data_update_pre_login_v2(cls, auth_type=None, email=None,
                                             country_code=None,
                                             phone_number=None,
                                             verify_token=None, client_id=None,
                                             client_secret=None,
                                             scopes='read write update delete'):
        if auth_type == UserRegistrationType.EMAIL.value and email:
            try:
                user = IBUser.objects.get(email=email)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The email address that you\'ve entered doesn\'t match any account.')),
                    res_status='')

            if user.email != email:
                raise BadRequest(str(_('Invalid email to verify')),
                                 res_status='')

            from ib_users.models.user_otp import UserOTP
            is_validated = UserOTP.validate_otp(user, verify_token, auth_type)
            if not is_validated:
                raise Forbidden(str(_('Invalid OTP')), res_status='')

            try:
                change_history = ChangeHistory.objects.get(user_id=user.id,
                                                           old_val='',
                                                           new_val=email,
                                                           is_verified=False)
                change_history.is_verified = True
                change_history.save()
            except ChangeHistory.DoesNotExist:
                raise BadRequest(str(_('Invalid OTP Verification')),
                                 res_status='')

            # ChangeHistory.create_change_history(user.id, '', user.email, True,
            #                                     auth_type)

            user.is_email_verified = True
            cls.remove_linked_email_or_phone_number(email=email)
            user.save()

        elif auth_type == UserRegistrationType.PHONE_NUMBER.value and phone_number:
            try:
                user = IBUser.objects.get(phone_number=phone_number,
                                          country_code=country_code)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The phone number that you\'ve entered doesn\'t match any account.')),
                    res_status='')

            if user.phone_number != phone_number or \
                            user.country_code != country_code:
                raise BadRequest(str(_('Invalid phone number to verify')),
                                 res_status='')

            from ib_users.models.user_otp import UserOTP
            is_validated = UserOTP.validate_otp(user, verify_token, auth_type)
            if not is_validated:
                raise Forbidden(str(_('Invalid OTP')), res_status='')

            new_phone_number = country_code + "," + phone_number
            try:
                change_history = ChangeHistory.objects.get(
                    user_id=user.id,
                    old_val='',
                    new_val=new_phone_number,
                    is_verified=False
                )
                change_history.is_verified = True
                change_history.save()
            except ChangeHistory.DoesNotExist:
                raise BadRequest(str(_('Invalid OTP Verification')),
                                 res_status='')

            # ChangeHistory.create_change_history(user.id, '', user.phone_number,
            #                                     True, auth_type)


            user.is_phone_verified = True
            cls.remove_linked_email_or_phone_number(
                phone_number=phone_number,
                country_code=country_code
            )
            user.save()

        else:
            raise Forbidden(str(_('\'auth_type\' is not correct.'
                                  )), res_status='')

        callback_dict = {
            'auth_type': auth_type,
            'username': user.username,
            'phone_number': phone_number,
            'country_code': country_code,
            'email': email,
            'm_id': user.id,
            'user_id': user.id,
            'm_username': user.username,
            'm_name': user.name,
            'm_pic': user.pic,
            'm_pic_thumbnail': user.pic_thumbnail
        }
        cls.signal_for_new_user_register_verify_evaluate(
            user_callback_dict=callback_dict)

        return get_oauth_details_response(user, client_id, client_secret,
                                          scopes)

    @classmethod
    def user_logout(cls, user, access_token, device_info=None, source=None):
        access_token_object = AccessToken.objects.get(user=user,
                                                      token=access_token)
        access_token_object.expires = datetime.now()
        access_token_object.save()
        callback_dict = {}
        if device_info:
            callback_dict.update(device_info)
        from ib_common.utilities.callback_wrapper import callback_wrapper
        from ib_users.utilities.signals import ib_user_logout_signal
        if source:
            callback_wrapper(source, 'ib_users', 'user_logout', access_token,
                             1, callback_dict, ib_user_logout_signal,
                             user)
        return {"success": True}

    @classmethod
    def activate_or_deactivate_account(cls, username=None, make_active=None):
        user = cls.objects.get(username=username)
        ChangeHistory.create_change_history(user.id, user.is_active,
                                            make_active, True, 'activation')
        user.is_active = make_active
        if not make_active:
            AccessToken.objects.filter(user=user).delete()
            RefreshToken.objects.filter(user=user).delete()
        user.save()
        return {"success": True}

    @classmethod
    def set_user_language(cls, username=None, language=None):
        user = cls.objects.get(username=username)
        user.language = language
        user.save()
        return {"success": True}

    @classmethod
    def resend_otp_v2(cls, username, auth_type, phone_number, country_code,
                      email, client_id, client_secret):
        if auth_type == UserRegistrationType.EMAIL.value:
            try:
                user = IBUser.objects.get(email=email)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The email address that you\'ve entered doesn\'t match any account.')),
                    res_status='')
        elif auth_type == UserRegistrationType.PHONE_NUMBER.value:
            try:
                user = IBUser.objects.get(phone_number=phone_number,
                                          country_code=country_code)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The phone number that you\'ve entered doesn\'t match any account.')),
                    res_status='')
        elif auth_type == UserRegistrationType.USERNAME.value:
            try:
                user = IBUser.objects.get(username=username)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The username that you\'ve entered doesn\'t match any account.')),
                    res_status='')
            auth_type = UserRegistrationType.EMAIL_AND_PHONE_NUMBER.value
        else:
            from django_swagger_utils.drf_server.exceptions.bad_request import \
                BadRequest
            raise BadRequest(str(_('Auth type not valid')), res_status='')
        from ib_users.models.user_otp import UserOTP
        UserOTP.send_otp(user, auth_type)
        return {'res_status': "Success", 'user_id': user.id}

    @classmethod
    def get_user_from_verified_auth(cls, auth_type=None, phone_number=None,
                                    country_code=None, email=None):
        if auth_type == UserRegistrationType.EMAIL.value:
            try:
                user = IBUser.objects.get(email=email, is_email_verified=True)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The email address that you\'ve entered doesn\'t match any account.')))
        elif auth_type == UserRegistrationType.PHONE_NUMBER.value:
            try:
                user = IBUser.objects.get(phone_number=phone_number,
                                          country_code=country_code,
                                          is_phone_verified=True)
            except IBUser.DoesNotExist:
                raise NotFound(str(_(
                    'The phone number that you\'ve entered doesn\'t match any account.')))
        else:
            from django_swagger_utils.drf_server.exceptions.bad_request import \
                BadRequest
            raise BadRequest(str(_('Auth type not valid')), res_status='')
        return user

    @classmethod
    def resend_otp_v2_for_data_verification(cls, user, auth_type=None,
                                            phone_number=None,
                                            country_code=None, email=None):

        if auth_type == UserRegistrationType.EMAIL.value and email is not None:
            try:
                change_history = ChangeHistory.objects.get(user_id=user.id,
                                                           old_val=user.email,
                                                           is_verified=False)
                if email != change_history.new_val:
                    raise BadRequest(str(_(
                        'change request\'s email and current request\'s  email are not matched')))

            except ChangeHistory.DoesNotExist:
                raise BadRequest(
                    str(_('No change email request is registered')))

        elif auth_type == UserRegistrationType.PHONE_NUMBER.value and phone_number is not None:

            old_complete_phone_number = user.country_code + "," + user.phone_number
            new_phone_number = country_code + "," + phone_number
            try:
                change_history = ChangeHistory.objects.get(user_id=user.id,
                                                           old_val=old_complete_phone_number,
                                                           is_verified=False)

                if change_history.new_val != new_phone_number:
                    raise BadRequest(
                        str(_(
                            'change request\'s phone number and current request\'s  phone number are not matched')))

            except ChangeHistory.DoesNotExist:
                raise BadRequest(
                    str(_('No change phone number request is registered')))

        else:
            raise BadRequest(str(_('\'auth_type\' is not correct.')))

        # todo sending new otp or old otp ?
        from ib_users.models.user_otp import UserOTP
        UserOTP.send_otp(user, auth_type, phone_number=phone_number,
                         email=email, country_code=country_code)
        return {"success": True}

    @staticmethod
    def dispatch_signal(user_callback_dict, source=None, access_token=None,
                        signal_obj=None, operation_id=None,
                        user=None):
        call_back_dict = {
            'callback_type': 'ib_users_service',
        }
        call_back_dict.update(user_callback_dict)
        from ib_common.utilities.callback_wrapper import callback_wrapper
        callback_wrapper(source, 'ib_users', operation_id, access_token, 1,
                         call_back_dict, signal_obj, user)

    @classmethod
    def signal_for_new_user_registered_evaluate(cls, user_callback_dict,
                                                user=None, source=None,
                                                access_token=None):
        signal_message = 'New User Registered'
        call_back_dict = {
            'message': signal_message
        }
        call_back_dict.update(user_callback_dict)
        from ib_users.utilities.signals import ib_user_registered_signal
        cls.dispatch_signal(call_back_dict, source, access_token,
                            ib_user_registered_signal, 'register_user_v2',
                            user)

    @classmethod
    def signal_for_new_user_register_verify_evaluate(cls, user_callback_dict,
                                                     user=None, source=None,
                                                     access_token=None):
        signal_message = 'New User Registered and Verified'
        call_back_dict = {
            'message': signal_message
        }
        call_back_dict.update(user_callback_dict)
        from ib_users.utilities.signals import \
            ib_user_registration_verification_signal
        cls.dispatch_signal(call_back_dict, source, access_token,
                            ib_user_registration_verification_signal,
                            'verify_data_update_pre_login_v2', user)

    @classmethod
    def signal_for_user_activated_evaluate(cls, user_callback_dict, user=None,
                                           source=None,
                                           access_token=None):
        signal_message = 'User account activated'
        call_back_dict = {
            'message': signal_message
        }
        call_back_dict.update(user_callback_dict)
        from ib_users.utilities.signals import ib_user_activated_signal
        cls.dispatch_signal(call_back_dict, source, access_token,
                            ib_user_activated_signal, 'login_user_v2', user)

    @classmethod
    def check_username_availability(cls, username=None):
        user_with_username = cls.objects.filter(username=username)
        if user_with_username.exists():
            response = {
                "res_status": "NOT_AVAILABLE"
            }
        else:
            response = {
                "res_status": "AVAILABLE"
            }

        return response

    @classmethod
    def user_login_v2_with_otp(cls, auth_type=None, phone_number=None,
                               email=None, country_code=None):
        user = cls.get_user_from_verified_auth(auth_type=auth_type,
                                               phone_number=phone_number,
                                               country_code=country_code,
                                               email=email)
        from ib_users.models.user_otp import UserOTP
        UserOTP.send_otp(user, auth_type)
        return {"success": True}

    @classmethod
    def user_login_v2_verify_otp(cls, auth_type=None, email=None,
                                 country_code=None, phone_number=None,
                                 verify_token=None, client_id=None,
                                 client_secret=None,
                                 scopes='read write update delete'):
        user = cls.get_user_from_verified_auth(auth_type=auth_type,
                                               phone_number=phone_number,
                                               country_code=country_code,
                                               email=email)
        from ib_users.models.user_otp import UserOTP
        is_validated = UserOTP.validate_otp(user, verify_token, auth_type)
        if not is_validated:
            raise Forbidden(str(_('Invalid OTP')), res_status='')
        return get_oauth_details_response(user, client_id, client_secret,
                                          scopes)

    @classmethod
    def resend_otp_v2_for_verified_auth(cls, auth_type=None, phone_number=None,
                                        country_code=None, email=None):
        user = cls.get_user_from_verified_auth(auth_type=auth_type,
                                               phone_number=phone_number,
                                               country_code=country_code,
                                               email=email)
        # todo sending new otp or old otp ?
        from ib_users.models.user_otp import UserOTP
        UserOTP.send_otp(user, auth_type)
        return {"success": True}

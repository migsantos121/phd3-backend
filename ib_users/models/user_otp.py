import time

from django.db import models
from django_swagger_utils.drf_server.exceptions.bad_request import BadRequest
from ib_common.models.abstract_date_time_model import AbstractDateTimeModel

from ib_users.constants.user_reg_type import UserRegistrationType
from ib_users.utilities.crypto import hash_otp



__author__ = 'tanmay.ibhubs'


class UserOTP(AbstractDateTimeModel):
    ib_user = models.ForeignKey('ib_users.IBUser', on_delete=models.CASCADE)
    otp_token = models.CharField(null=False, max_length=128)
    auth_type = models.CharField(default='phone_number', max_length=100)
    expiry_time = models.BigIntegerField(null=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'ib_users'

    def __unicode__(self):
        return str(self.ib_user) + "/" + str(self.is_active)

    def reset_expiry_time(self):
        self.expiry_time += 3600
        self.save()
        return

    @classmethod
    def create_otp(cls, ib_user, auth_type):

        current_time = int(time.time())
        try:
            user_otp = cls.objects.get(ib_user=ib_user, expiry_time__gte=current_time, auth_type=auth_type,
                                       is_active=True)
            user_otp.is_active = False
            user_otp.save()
        except UserOTP.DoesNotExist:
            pass

        from ib_users.utilities.generate_otp import generate_otp
        gen_token = str(generate_otp(ib_user.username))
        otp_token = hash_otp(gen_token)
        print 'otp_token: ', otp_token
        user_otp = UserOTP(ib_user=ib_user,
                           otp_token=otp_token,
                           auth_type=auth_type,
                           expiry_time=current_time,
                           is_active=True)

        user_otp.reset_expiry_time()

        return user_otp, gen_token

    @staticmethod
    def send_otp_sms(phone_number, country_code, otp_token):

        if country_code is None:
            country_code = ""

        from django.conf import settings
        _template = settings.VERIFY_USER_OTP_SMS_TEMPLATE

        import importlib
        _template_module = importlib.import_module(_template)
        verify_user_otp = _template_module.VERIFY_USER_OTP

        message = verify_user_otp.format(otp_token=str(otp_token))
        mobile_number = country_code.replace("+", "") + phone_number
        from ib_users.utilities.send_sms import send_sms
        send_sms(mobile_numbers=[mobile_number], message=message)

    @staticmethod
    def send_otp_email(email, otp_token):
        from django.conf import settings

        data_dict = {
            "otp_token": str(otp_token)
        }

        _template = settings.VERIFY_USER_OTP_EMAIL_TEMPLATE
        import importlib
        _template_module = importlib.import_module(_template)

        from django.template import Template
        serializer_template = Template(_template_module.VERIFY_USER_OTP)
        from django.template import Context
        context = Context(data_dict)
        html_content = serializer_template.render(context)

        subject = _template_module.VERIFY_USER_OTP_SUBJECT

        from ib_users.utilities.send_mail import send_mail
        send_mail(
            subject=subject,
            sender="",
            receiver=email,
            text="",
            html_content=html_content
        )

    @classmethod
    def send_otp(cls, ib_user, auth_type, phone_number=None, country_code=None,
                 email=None):
        if phone_number is None:
            phone_number = ib_user.phone_number
        if country_code is None:
            country_code = ib_user.country_code
        if email is None:
            email = ib_user.email

        if auth_type == UserRegistrationType.EMAIL.value:
            user_otp, otp_token = UserOTP.create_otp(ib_user, auth_type)
            cls.send_otp_email(email=email, otp_token=otp_token)

        elif auth_type == UserRegistrationType.PHONE_NUMBER.value:
            user_otp, otp_token = UserOTP.create_otp(ib_user, auth_type)
            cls.send_otp_sms(phone_number=phone_number,
                             country_code=country_code,
                             otp_token=otp_token)

        elif auth_type == UserRegistrationType.EMAIL_AND_PHONE_NUMBER.value:
            otp_sent = False
            if ib_user.phone_number:
                user_otp, otp_token = UserOTP.create_otp(ib_user, UserRegistrationType.PHONE_NUMBER.value)
                cls.send_otp_sms(phone_number=phone_number,
                                 country_code=country_code,
                                 otp_token=otp_token)
                otp_sent = True

            if ib_user.email:
                user_otp, otp_token = UserOTP.create_otp(ib_user, UserRegistrationType.EMAIL.value)
                cls.send_otp_email(email=email, otp_token=otp_token)
                otp_sent = True

            if not otp_sent:
                from django_swagger_utils.drf_server.exceptions.expectation_failed import ExpectationFailed
                raise ExpectationFailed('No phone number or email on record for this user.', res_status=False)

        elif auth_type == UserRegistrationType.USERNAME.value:
            otp_sent = False
            if ib_user.phone_number:
                user_otp, otp_token = UserOTP.create_otp(ib_user, UserRegistrationType.PHONE_NUMBER.value)
                cls.send_otp_sms(phone_number=phone_number,
                                 country_code=country_code,
                                 otp_token=otp_token)
                otp_sent = True

            if ib_user.email:
                user_otp, otp_token = UserOTP.create_otp(ib_user, UserRegistrationType.EMAIL.value)
                cls.send_otp_email(email=email, otp_token=otp_token)
                otp_sent = True

            if not otp_sent:
                pass


        else:
            raise BadRequest('BAD_REQUEST_ERROR: auth_type=phone_number|email|email_and_phone_number')

    @classmethod
    def validate_otp(cls, ib_user, otp_token, auth_type):
        current_time = int(time.time())
        try:
            if auth_type == UserRegistrationType.USERNAME.value:
                try:
                    auth_type = UserRegistrationType.EMAIL.value
                    user_otp = cls.objects.get(ib_user=ib_user, expiry_time__gte=current_time, auth_type=auth_type,
                                               is_active=True)
                except UserOTP.DoesNotExist:
                    auth_type = UserRegistrationType.PHONE_NUMBER.value
                    user_otp = cls.objects.get(ib_user=ib_user, expiry_time__gte=current_time, auth_type=auth_type,
                                               is_active=True)
            else:
                user_otp = cls.objects.get(ib_user=ib_user, expiry_time__gte=current_time, auth_type=auth_type,
                                           is_active=True)
            if user_otp.otp_token == hash_otp(otp_token):
                user_otp.is_active = False
                user_otp.save()
                return True
            return False
        except Exception as e:
            print "Validate OTP Exception ---> ", e
            return False

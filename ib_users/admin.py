from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from ib_users.models.change_history import ChangeHistory
from ib_users.models.ib_user import IBUser
from ib_users.models.otp_details import OTPDetails
from ib_users.models.registration_source import RegistrationSource
from ib_users.models.social_provider import SocialProvider
from ib_users.models.user_otp import UserOTP
from ib_users.models.user_social_provider import UserSocialProvider
from ib_users.models.user_extra_data import UserExtraData
from ib_users.models.ib_user_registration_source import IBUserRegistrationSource

User = get_user_model()


class IBUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'name', 'is_deleted']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('name', 'first_name', 'last_name', 'email', 'language',
                                        'pic', 'pic_thumbnail', 'gender', 'phone_number',
                                        'country_code', 'is_email_verified', 'is_phone_verified')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class OTPDetailsAdmin(admin.ModelAdmin):
    list_display = ['otp_count', 'user_name']

    def user_name(self, obj):
        return obj.ib_user.username


class UserExtraDataAdmin(admin.ModelAdmin):
    list_display = ['ib_user', 'user_name', 'ud_key', 'ud_value']

    def user_name(self, obj):
        return obj.ib_user.username


class RegistrationSourceAdmin(admin.ModelAdmin):
    list_display = ['registration_source']


class UserOTPAdmin(admin.ModelAdmin):
    list_display = ['id', 'ib_user', 'is_active', 'expiry_time', 'auth_type']


class ChangeHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'old_val', 'new_val', 'type']


class SocialProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class UserSocialProviderAdmin(admin.ModelAdmin):
    list_display = ['ib_user', 'social_provider', 'social_token', 'extra_info']


class IBUserRegistrationSourceAdmin(admin.ModelAdmin):
    list_display = ['ib_user', 'registration_source']


admin.site.register(IBUser, IBUserAdmin)
admin.site.register(OTPDetails, OTPDetailsAdmin)
admin.site.register(RegistrationSource, RegistrationSourceAdmin)
admin.site.register(UserOTP, UserOTPAdmin)
admin.site.register(ChangeHistory, ChangeHistoryAdmin)
admin.site.register(SocialProvider, SocialProviderAdmin)
admin.site.register(UserSocialProvider, UserSocialProviderAdmin)
admin.site.register(UserExtraData, UserExtraDataAdmin)
admin.site.register(IBUserRegistrationSource, IBUserRegistrationSourceAdmin)
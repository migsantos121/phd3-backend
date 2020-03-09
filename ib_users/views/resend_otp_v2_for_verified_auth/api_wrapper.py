
from .validator_class import ValidatorClass
from django_swagger_utils.drf_server.utils.decorator.interface_decorator import validate_decorator


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    from ib_users.models import IBUser
    response = IBUser.resend_otp_v2_for_verified_auth(**kwargs["request_data"])
    return response
    


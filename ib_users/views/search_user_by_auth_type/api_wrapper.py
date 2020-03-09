
from .validator_class import ValidatorClass
from django_swagger_utils.drf_server.utils.decorator.interface_decorator import validate_decorator


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    request_data = kwargs["request_data"]
    auth_type = request_data['auth_type']
    username = request_data.get('username')
    phone_number = request_data.get('phone_number')
    email = request_data.get('email')
    country_code = request_data.get('country_code')

    source = kwargs['source']

    from ib_users.models import IBUser
    response_object = IBUser.search_user_by_auth_type(auth_type=auth_type, username=username, phone_number=phone_number,
                                                      email=email, country_code=country_code, source=source)
    return response_object

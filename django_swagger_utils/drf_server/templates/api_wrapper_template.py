apiwrapper = """{% autoescape off %}
from .validator_class import ValidatorClass
from django_swagger_utils.drf_server.utils.decorator.interface_decorator import validate_decorator


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    # ------------------------------------MOCK IMPLEMENTATION-------------------------------------
    from {{app_name}}.views.{{operation_id}}.tests.test_case_01 import test_case
    from django_swagger_utils.drf_server.utils.server_gen.mock_response import mock_response
    response_tuple = mock_response(app_name="{{app_name}}", operation_name="{{operation_id}}", test_case=test_case,
                                   kwargs=kwargs)
    return response_tuple[1]
    
{% endautoescape%}
"""

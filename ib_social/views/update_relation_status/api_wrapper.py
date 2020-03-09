from .validator_class import ValidatorClass
from django_swagger_utils.drf_server.utils.decorator.interface_decorator import validate_decorator

@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args,**kwargs):

    #------------------start of mock implementation-------------------------------------
    #comment below lines and return response dict
    from ib_social.views.update_relation_status.tests.test_case_01 import test_case
    from django_swagger_utils.drf_server.utils.server_gen.mock_response import mock_response
    response_tuple = mock_response(app_name="ib_social", operation_name="update_relation_status", test_case=test_case,
                                       kwargs=kwargs)
    return response_tuple[1]
    #-------------------end of mock implementation---------------------------------------
    #response_object={
    #   "example_key":"example_value",
    #}
    #return response_object
    #--------------------end of api implementation--------------------------------------

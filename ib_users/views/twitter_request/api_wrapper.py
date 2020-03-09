from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator
from .validator_class import ValidatorClass


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    # ---------MOCK IMPLEMENTATION---------
    try:
        from ib_users.views.twitter_request.tests.test_case_01 \
            import TEST_CASE as test_case
    except ImportError:
        from ib_users.views.twitter_request.tests.test_case_01 \
            import test_case
    
    from django_swagger_utils.drf_server.utils.server_gen.mock_response \
        import mock_response
    response_tuple = mock_response(
        app_name="ib_users", test_case=test_case,
        operation_name="twitter_request",
        kwargs=kwargs)
    return response_tuple[1]

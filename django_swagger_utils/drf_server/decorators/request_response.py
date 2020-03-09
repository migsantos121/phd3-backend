# coding=utf-8
import importlib

__author__ = 'anush0247'


def get_defaults(app_name):
    from django_swagger_utils.drf_server.default.request_response import REQUEST_RESPONSE_DECORATOR
    default_options = REQUEST_RESPONSE_DECORATOR

    from django_swagger_utils.drf_server.default.request_response import SECURITY_DEFINITIONS
    security_definitions = SECURITY_DEFINITIONS

    if app_name:
        default_options = getattr(importlib.import_module("%s.build.request_response.decorator_options" % app_name),
                                  "REQUEST_RESPONSE_DECORATOR")
        security_definitions = getattr(importlib.import_module("%s.build.request_response.security_definitions" %
                                                               app_name), "SECURITY_DEFINITIONS")
    return default_options, security_definitions


def configure_options(options, app_name):
    options = {} if options is None else options
    default_options, security_definitions = get_defaults(app_name)

    for key in default_options.keys():
        if options.get(key) is None:
            options[key] = default_options[key]

    securities = options.get("SECURITY", [])
    options["PERMISSIONS_REQUIRED"] = []
    options["AUTHENTICATION_CLASSES"] = []
    options["SCOPES_REQUIRED"] = []

    for security in securities:

        security_def = security_definitions[security]
        options["SCOPES_REQUIRED"].extend(securities[security])
        options["PERMISSIONS_REQUIRED"].extend(security_def["PERMISSIONS_REQUIRED"])
        if security_def["TYPE"] != "API_KEY":
            options["AUTHENTICATION_CLASSES"].extend(security_def["AUTHENTICATION_CLASSES"])
    return options


def request_response(options=None, app_name=None, operation_id=None):
    options = configure_options(options, app_name=app_name)

    def decorator(function):
        from django_swagger_utils.drf_server.decorators.wrap_exceptions import wrap_exceptions
        from django_swagger_utils.drf_server.decorators.response_time import response_time
        from rest_framework.decorators import api_view
        from rest_framework.decorators import authentication_classes
        from rest_framework.decorators import permission_classes
        from django_swagger_utils.drf_server.decorators.conditional_decorator import conditional_decorator
        from oauth2_provider.decorators import protected_resource
        from rest_framework.decorators import parser_classes
        from rest_framework.decorators import renderer_classes

        @response_time(app_name=app_name, operation_id=operation_id)
        @wrap_exceptions()
        @api_view([options['METHOD']])  # Applying the specified request method
        @authentication_classes(options["AUTHENTICATION_CLASSES"])
        @permission_classes(options['PERMISSIONS_REQUIRED'])  # Applying the list of permissions specified
        @conditional_decorator(dec=protected_resource(scopes=options['SCOPES_REQUIRED']),
                               condition=len(options['SCOPES_REQUIRED']))
        @parser_classes(options['PARSER_CLASSES'])
        @renderer_classes(options['RENDERER_CLASSES'])
        def handler(*args, **kwargs):
            from django_swagger_utils.drf_server.wrappers.request_response_wrapper import RequestResponseWrapper
            from time import time
            a = time()
            request = args[0]
            req_res = RequestResponseWrapper(request=request, options=options, kwargs=kwargs)
            kwargs = req_res.pre_execution()
            function_return_value = function(*args, **kwargs)
            return_value = req_res.post_execution(function_return_value)

            from django.conf import settings
            insert_last_access_required = getattr(settings, 'INSERT_LAST_ACCESS_REQUIRED', 'TRUE')
            if insert_last_access_required == 'TRUE':
                insert_last_access(request, app_name, operation_id)
            b = time()
            print "API Execution Time: %s" % str(b - a)
            return return_value

        handler.__doc__ = function.__doc__
        return handler

    return decorator


def insert_last_access(request, app_name, operation_id):
    user = request.user

    from django.contrib.auth.models import AnonymousUser
    if user.is_authenticated and not isinstance(user, AnonymousUser):
        from django_swagger_utils.models import LastAccess
        last_access_object, created = LastAccess.objects.get_or_create(
            app_name=app_name,
            operation_id=operation_id,
            user=user
        )
        last_access_object.save()

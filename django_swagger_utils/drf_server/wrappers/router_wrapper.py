# coding=utf-8
import importlib


def router_wrapper(app_name, url_path, operations_dict, request, *args, **kwargs):
    view_name = operations_dict.get(request.method, None)
    if view_name:
        import_str = "%s.build.view_environments.%s.%s.%s" % (app_name, url_path,view_name, view_name)
        view_def = getattr(importlib.import_module(import_str), view_name)
        response = view_def(request, *args, **kwargs)
    else:
        from django_swagger_utils.drf_server.exceptions.method_not_allowed import MethodNotAllowed
        raise MethodNotAllowed("Method Not Allowed")
    return response

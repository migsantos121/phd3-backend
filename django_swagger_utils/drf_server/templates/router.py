ROUTER = """{% autoescape off %}path_method_dict = {{ path_method_dict_str }}


def {{path_method_name}}(request, *args, **kwargs):
    from django_swagger_utils.drf_server.utils.server_gen.get_operations_dict import get_operations_dict
    operations_dict = get_operations_dict(path_method_dict, request.path)

    from django_swagger_utils.drf_server.wrappers.router_wrapper import router_wrapper
    response = router_wrapper("{{app_name}}", "{{path_method_name}}", operations_dict, request, *args, **kwargs)
    return response{% endautoescape %}
"""
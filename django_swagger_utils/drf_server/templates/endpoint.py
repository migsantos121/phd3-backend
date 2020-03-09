ENDPOINT = """{% autoescape off %}{% for import_str in imports_list %}{{ import_str }}
{% endfor %}

options = {
    'METHOD': '{{request_method}}',
    'REQUEST_WRAPPING_REQUIRED': {{request_wrapping|title}},
    'REQUEST_ENCRYPTION_REQUIRED': {{request_encryption|title}},
    'REQUEST_IS_PARTIAL': False,
    'PARSER_CLASSES': [
        {% for consume in consumes %}PARSER_MAPPING["{{ consume }}"]{% if not forloop.last %},
        {% endif %}{% endfor %}
    ],
    'RENDERER_CLASSES': [
        {% for produce in produces %}RENDERER_MAPPING["{{ produce }}"]{% if not forloop.last %},
        {% endif %}{% endfor %}
    ],
    'REQUEST_QUERY_PARAMS_SERIALIZER': {{request_query_params_serializer}},
    'REQUEST_HEADERS_SERIALIZER': {{request_headers_serializer}},
    'REQUEST_SERIALIZER': {{request_body_serializer}},
    'REQUEST_SERIALIZER_MANY_ITEMS': {{request_body_serializer_is_array|title}},
    'RESPONSE': {
        {% for response_method, each_response in responses.items %}
        '{{response_method}}' : {
           'RESPONSE_SERIALIZER': {{each_response.response_serializer}},
           'RESPONSE_SERIALIZER_MANY_ITEMS':  {{each_response.response_serializer_is_array|title}},
           'HEADERS_SERIALIZER': {{each_response.response_headers_serializer}},
        }
        {% if not forloop.last %},
        {% endif %}{% endfor %}
    },
    "SECURITY": {{% for decorator in securities %}{% for security_name, scopes in decorator.items %}
        "{{security_name}}" : [
            {% for scope in scopes %}"{{ scope }}"{% if not forloop.last %},{% endif %}
            {% endfor %}
        ]{% endfor %}{% if not forloop.last %},{% endif %}{% endfor %}
    }
}

app_name = "{{app_name}}"
operation_id  = "{{operation_id}}"

@request_response(options=options, app_name=app_name, operation_id=operation_id)
def {{operation_id}}(request, *args, **kwargs):
    args = (request,) + args
    from django_swagger_utils.drf_server.wrappers.view_env_wrapper import view_env_wrapper
    return view_env_wrapper(app_name, "{{operation_id}}", *args, **kwargs)
{% endautoescape %}
"""

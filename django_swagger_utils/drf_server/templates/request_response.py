REQUEST_RESPONSE_DECORATOR_TEMPLATE = """from django_swagger_utils.drf_server.default.parser_mapping import PARSER_MAPPING
from django_swagger_utils.drf_server.default.renderer_mapping import RENDERER_MAPPING

from django.conf import settings
django_swagger_utils_settings = settings.SWAGGER_UTILS
defaults = django_swagger_utils_settings["DEFAULTS"]


REQUEST_RESPONSE_DECORATOR = {
    'METHOD': 'POST',
    'REQUEST_WRAPPING_REQUIRED': defaults.get("REQUEST_WRAPPING_REQUIRED", True),
    'REQUEST_ENCRYPTION_REQUIRED': defaults.get("REQUEST_ENCRYPTION_REQUIRED", False),
    'REQUEST_IS_PARTIAL': False,
    'REQUEST_SERIALIZER_MANY_ITEMS': False,
    'RESPONSE_SERIALIZER_MANY_ITEMS': False,
    'PARSER_CLASSES': [
        {% for consume in consumes %}PARSER_MAPPING["{{consume}}"]{% if not forloop.last %},
        {% endif %}{% endfor %}
    ],
    'RENDERER_CLASSES': [
        {% for produce in produces %}RENDERER_MAPPING["{{produce}}"]{% if not forloop.last %},
        {% endif %}{% endfor %}
    ],
    "SECURITY": {{% for decorator in securities %}{% for security_name, scopes in decorator.items %}
        "{{security_name}}" : [
            {% for scope in scopes %}"{{ scope }}"{% if not forloop.last %}, {% endif %}
            {% endfor %}
        ]{% endfor %}{% if not forloop.last %},{% endif %}{% endfor %}
    },
    'REQUEST_SERIALIZER': None,
    'RESPONSE': {
        '200': {
            'CONTENT_TYPE': "application/json",
            'RESPONSE_SERIALIZER': None,
            'HEADERS_SERIALIZER': None,
        }
    }
}

"""

SECURITY_DEFINITIONS_TEMPLATE = """{% autoescape off %}from oauth2_provider.ext.rest_framework import OAuth2Authentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django_swagger_utils.drf_server.utils.server_gen.is_valid_api_key import IsValidAPIKey

SECURITY_DEFINITIONS = {{% for decorator in security_definitions %}
    "{{ decorator.SECURITY_NAME }}" : {
        "TYPE": "{{decorator.TYPE}}",
        "AUTHENTICATION_CLASSES": [{{ decorator.AUTHENTICATION_CLASSES | join:', ' }}],
        "PERMISSIONS_REQUIRED": [{{ decorator.PERMISSIONS_REQUIRED | join:', ' }}],
        "SCOPES_REQUIRED": [{{ decorator.SCOPES_REQUIRED | join:', ' }}]
    }{% if not forloop.last %},{% endif %}{% endfor %}
}
{% endautoescape %}

"""

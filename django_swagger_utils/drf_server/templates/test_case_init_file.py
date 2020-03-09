TESTS_INIT_FILE = """{% autoescape off %}# Endpoint Configuration

APP_NAME = "{{app_name}}"
OPERATION_NAME = "{{operation_id}}"
REQUEST_METHOD = "{{request_method|lower}}"
URL_SUFFIX = "{{example_path_url}}"

{% for test_case, test_case_class  in test_cases.items %}
from .{{test_case}} import {{test_case_class}}{% endfor %}

__all__ = [
    {% for test_case, test_case_class  in test_cases.items %}"{{test_case_class}}"{% if not forloop.last %},
    {% endif %}{% endfor %}
]

{% endautoescape%}
"""

TESTS_INIT_FILE = """{% autoescape off %}{% for operation_id in operation_ids %}
from .{{operation_id}} import {{operation_id}}APITestCase{% endfor %}


__all__ = [
    {% for operation_id in operation_ids %} "{{operation_id}}APITestCase"{% if not forloop.last %},
    {% endif %}{% endfor %}
]
{% endautoescape%}
"""
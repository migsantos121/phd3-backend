ENVIRONMENT_MAPPING = """{% autoescape off %}view_environments_mapping = {
    {% for operation_id, operation_value in mapping_dict.items %}"{{operation_id}}":  "{{operation_value}}",
    {% endfor%}}{% endautoescape %}
"""
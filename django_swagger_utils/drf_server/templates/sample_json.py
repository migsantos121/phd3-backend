SAMPLE_JSON = """{% autoescape off %}
{% if request_body_sample_json %}
REQUEST_BODY_JSON = \"\"\"
{{request_body_sample_json}}
\"\"\"
{% endif %}
{% for response_method, each_response in responses.items %}{% if each_response.response_serializer_sample_json %}
RESPONSE_{{response_method}}_JSON = \"\"\"
{{each_response.response_serializer_sample_json}}
\"\"\"
{% endif %}{% endfor %}{% endautoescape%}
"""
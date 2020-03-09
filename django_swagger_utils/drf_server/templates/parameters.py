PARAMETER = """{% autoescape off %}class {{param_name_camel_case}}Parameter(object):
    @staticmethod
    def get_param_name():
        param_names = {
            "parameter_name": "{{param_name}}",
            "parameter_field_name": "{{param_field_name}}"
        }
        return param_names

    @staticmethod
    def get_serializer_class():{% if param_serializer %}
        serializer_options = {
            "param_serializer": "{{param_serializer}}",
            "param_serializer_import_str": "{{param_serializer_import_str}}",
            "param_serializer_required": {{param_serializer_required|title}},
            "param_serializer_array": {{param_serializer_array|title}}
        }
        return serializer_options
        {% else %}
        pass{% endif %}

    @staticmethod
    def get_serializer_field():{% if param_serializer_field %}
        from rest_framework import serializers
        from django_swagger_utils.drf_server.fields.collection_format_field import CollectionFormatField
        return {{ param_serializer_field }}
        {% else %}
        pass{% endif %}

    @staticmethod
    def get_url_regex():{% if param_url_regex %}
        regex = r"{{ param_url_regex }}"
        return regex{% else %}
        pass{% endif %}{% endautoescape %}"""

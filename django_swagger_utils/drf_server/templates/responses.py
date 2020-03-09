RESPONSE = """{% autoescape off %}class {{response_name_camel_case}}Response(object):

    @staticmethod
    def get_response():
        response = {
            "response_data": '{{response_data_no_indent}}',
            "response_serializer": "{{response_serializer}}",
            "response_serializer_import_str": "{{response_serializer_import_str}}",
            "response_serializer_array": {{response_serializer_array|title}},
        }
        return response


    @staticmethod
    def get_response_headers_serializer():{% if response_headers_serializer %}
        headers_serializer_options = {
            "response_headers_serializer": "{{response_headers_serializer}}",
            "response_headers_serializer_import_str": "{{response_headers_serializer_import_str}}",
        }
        return headers_serializer_options
        {% else %}
        pass{% endif %}{% endautoescape %}"""

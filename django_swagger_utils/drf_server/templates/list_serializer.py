LIST_SERIALIZER = """from rest_framework import serializers


class {{serializer_camel_case_name}}Serializer(serializers.ListSerializer):
    child = {{field_string}}
"""

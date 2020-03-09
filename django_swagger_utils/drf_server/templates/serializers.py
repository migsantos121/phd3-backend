SERIALIZERS = """{% autoescape off %}from rest_framework import serializers

from django_swagger_utils.drf_server.utils.decorator.deserialize import deserialize
from django_swagger_utils.drf_server.utils.server_gen.type_file_utils import get_type_object
from django_swagger_utils.drf_server.utils.server_gen.type_file_utils import get_type_list_object
from django_swagger_utils.drf_server.fields.collection_format_field import CollectionFormatField


class {{serializer_camel_case_name}}Type(object):
    def __init__(self, {{ required_params | join:', ' }}{% if required_params%}, {%endif%}{% for param in optional_params %}{{ param }}=None, {% endfor%} **kwargs):{% for param in required_params %}
        self.{{param}} = {{param}}{% endfor %}{% for param in optional_params %}
        self.{{param}} = {{param}}{% endfor %}

    def __unicode__(self):
        from django_swagger_utils.drf_server.utils.server_gen.get_unicode_str import get_unicode_str
        return get_unicode_str(self)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __getitem__(self, item):
        return getattr(self, item)


class {{serializer_camel_case_name}}Serializer(serializers.Serializer):{% for param, prop in params.items %}{% if prop.serializer_import_str %}
    {{prop.serializer_import_str}}{% endif %}
    {{param}} = {{prop.field_string}}{% endfor %}

    def create(self, validated_data):{% for param, prop in object_params.items %}
        {% if prop.type == "object_array" %}{{prop.serializer_import_str}}
        {{param}}_val = []
        {{param}}_list_val = validated_data.pop("{{param}}", [])
        for each_data in {{param}}_list_val:
            each_obj = deserialize({{prop.type_file_class|slice:":-4"}}Serializer, each_data, many=False, partial=True)
            {{param}}_val.append(each_obj)
        {% elif prop.type == "object" %}{{prop.serializer_import_str}}
        {{param}}_val = deserialize({{prop.type_file_class|slice:":-4"}}Serializer, validated_data.pop("{{param}}", None), many=False, partial=True)
        {% endif %}{% endfor %}
        return {{serializer_camel_case_name}}Type({% for param, prop in object_params.items %}{% if prop.type == "object" or prop.type == "object_array" %}{{param}}={{param}}_val, {% endif %}{% endfor %}**validated_data)
{% endautoescape %}
"""

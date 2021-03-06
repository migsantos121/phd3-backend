ALL_OF_SERIALIZER = """{% for import_str in imports_list %}{{ import_str }}
{% endfor %}
from django_swagger_utils.drf_server.utils.decorator.deserialize import deserialize

class {{serializer_name}}Type({{ type_class_names | join:', ' }}):
    def __init__(self, **validated_data):
        {% for type_class_name in type_class_names %}{{ type_class_name }}.__init__(self, **validated_data)
        {% endfor %}

class {{serializer_name}}Serializer({{ serializer_class_names | join:', ' }}):
    def create(self, validated_data):
        {% for serializer_class_name in serializer_class_names %}
        {{serializer_class_name|slice:"1"|lower}}{{serializer_class_name|slice:"1:"}} = deserialize({{serializer_class_name}}, validated_data, many=False, partial=True)
        validated_data.update({{serializer_class_name|slice:"1"|lower}}{{serializer_class_name|slice:"1:"}}.__dict__)
        {% endfor %}
        return {{serializer_name}}Type(**validated_data)
"""

from django.template import Template, Context

from django_swagger_utils.drf_server.fields.boolean_field import boolean_field
from django_swagger_utils.drf_server.fields.integer_field import integer_field
from django_swagger_utils.drf_server.fields.number_field import number_field
from django_swagger_utils.drf_server.fields.string_field import string_field


class SerializerGenerator(object):
    fields = {}
    required = []
    def_type = None
    optional_params = []
    serializer_ref = None
    is_array = False
    all_of_props = []

    def __init__(self, schema_properties, serializer_name, paths, base_path, ):
        self.schema_properties = schema_properties
        self.serializer_name = serializer_name
        self.base_path = base_path
        self.paths = paths

    def generate_serializer_file(self):

        # setup configure
        self.configure()

        if self.all_of_props:
            serializer_dict = self.get_all_of_properties(self.serializer_name, self.all_of_props)
        elif self.serializer_ref:
            serializer_dict = self.process_ref_serializer()
        else:
            serializer_dict = self.process_non_ref_serializer()
        return serializer_dict

    def process_ref_serializer(self):
        serializer_dict = self.get_definition_ref_properties(self.serializer_ref)
        serializer_dict["field_string"] = serializer_dict["field_string"][:-2]
        serializer_dict["is_array_serializer"] = self.is_array
        return serializer_dict

    def configure(self):
        self.set_base_path()
        self.set_def_type()

    def set_base_path(self):
        self.base_path += "/" + self.serializer_name

    def process_non_ref_serializer(self):

        # set properties
        field_string = self.set_properties()
        if isinstance(field_string, str) and self.is_array:
            # creating a list serailizer
            self.is_array = False
            serializer_file_content = self.get_list_serializer_file_content(field_string)
        else:

            # set required fields
            self.set_required_fields()

            # processing fields
            field_properties, optional_params, object_params = self.process_serializer_fields()

            # rendering the serializer file contents
            serializer_file_content = self.serializer_file_contents(optional_params, field_properties, object_params)

        # write file
        self.write_serializer_file(serializer_file_content)

        return self.get_serializer_dict()

    def get_camel_case_serializer_name(self):

        from django_swagger_utils.core.utils.case_convertion import to_camel_case
        return to_camel_case(self.serializer_name)

    def set_properties(self):
        field_string = None
        self.fields = self.schema_properties.get("properties", None)
        if not self.fields:
            schema_type = self.schema_properties.get("type", "NoType")
            prop_required = True
            if schema_type == "integer":
                field_string = integer_field(self.schema_properties, prop_required)
            elif schema_type == "number":
                field_string = number_field(self.schema_properties, prop_required)
            elif schema_type == "string":
                field_string = string_field(self.schema_properties, prop_required)
            elif schema_type == "boolean":
                field_string = boolean_field(self.schema_properties, prop_required)
            else:
                raise Exception("Properties for %s not available" % self.serializer_name)
        return field_string

    def set_required_fields(self):
        self.required = self.schema_properties.get("required", [])

    def set_def_type(self):

        self.def_type = self.schema_properties.get("type", None)
        if not self.def_type:
            schema_ref = self.schema_properties.get("$ref", None)
            if not schema_ref:
                all_of_props = self.schema_properties.get("allOf", None)
                if not all_of_props:
                    raise Exception("'type' or 'schema' key missing for %s " % self.serializer_name)
                else:
                    self.all_of_props = all_of_props
            else:
                self.serializer_ref = schema_ref
        elif self.def_type == "array":
            self.is_array = True
            self.schema_properties = self.schema_properties.get("items")
            schema_ref = self.schema_properties.get("$ref", None)
            if schema_ref:
                self.serializer_ref = schema_ref

        elif self.def_type == "object":
            pass
        else:
            raise Exception("'type' key has invalid value in %s " % self.serializer_name)

    def get_field(self, prop_name, properties, prop_required):
        context_properties = {
            "serializer_import_str": "",
            "field_string": "",
            "type_file_import_str": "",
        }
        options = []
        if not prop_required:
            options.append("required=False")
        prop_ref = properties.get("$ref", None)
        prop_all_of = properties.get("allOf", None)
        if prop_all_of:
            context_properties = self.get_all_of_properties(prop_name, prop_all_of, options, is_instance=True)
        elif not prop_ref:
            prop_type = properties.get("type", None)
            if not prop_type:
                raise Exception("property 'type' not defined for '%s' in '%s' " % (prop_name, self.serializer_name))
            if prop_type == "integer":
                context_properties["field_string"] = integer_field(properties, prop_required)
            elif prop_type == "number":
                context_properties["field_string"] = number_field(properties, prop_required)
            elif prop_type == "string":
                context_properties["field_string"] = string_field(properties, prop_required)
            elif prop_type == "boolean":
                context_properties["field_string"] = boolean_field(properties, prop_required)
            elif prop_type == "array":
                context_properties = self.get_array_field(properties.get("items"), prop_name, options)
            elif prop_type == "object_array":
                context_properties = properties
            elif prop_type == "object":
                context_properties = self.get_object_properties(prop_name, properties, options)
                context_properties["type"] = "object"
        else:
            options.append("allow_null=True")
            context_properties = self.get_definition_ref_properties(prop_ref, options)

        properties.update(context_properties)
        return properties

    def get_all_of_properties(self, prop_name, prop_all_of, options=None, is_instance=False):
        if options is None:
            options = []
        imports_list = []
        type_class_names = []
        serializer_class_names = []

        for index, each_schema in enumerate(prop_all_of):
            schema_name = "Schema%d" % index
            base_path = self.base_path + "/" + prop_name
            serializer_generator = SerializerGenerator(schema_properties=each_schema, base_path=base_path,
                                                       serializer_name=schema_name, paths=self.paths)

            each_schema_context_properties = serializer_generator.generate_serializer_file()
            imports_list.append(each_schema_context_properties["serializer_import_str"])
            imports_list.append(each_schema_context_properties["type_file_import_str"])
            type_class_names.append(each_schema_context_properties["type_file_class"])
            serializer_class_names.append(each_schema_context_properties["field_string"])

        context_properties = self.generate_serializer_from_all_of_properties(prop_name, imports_list, type_class_names,
                                                                             serializer_class_names, options,
                                                                             is_instance)

        return context_properties

    def generate_serializer_from_all_of_properties(self, prop_name, imports_list, type_class_names,
                                                   serializer_class_names, options, is_instance):

        self.write_all_of_serializer_file(prop_name, imports_list, type_class_names, serializer_class_names)

        from django_swagger_utils.core.utils.convert_path_to_package_str import convert_path_to_package_str
        package_import_str = convert_path_to_package_str(self.base_path, self.paths['base_dir'])
        base_import_str = "from %s.%sSerializer" % (package_import_str, prop_name)
        options_str = ", ".join(options)
        field_string = "%sSerializer" % prop_name
        if is_instance:
            field_string = "%s(%s)" % (field_string, options_str)
        context_properties = {"type": "object",
                              "field_string": field_string,
                              "serializer_import_str": "%s import %sSerializer" % (base_import_str, prop_name),
                              "type_file_import_str": "%s import %sType" % (base_import_str, prop_name),
                              "type_file_class": "%sType" % prop_name,
                              "is_array_serializer": self.is_array}
        return context_properties

    def write_all_of_serializer_file(self, prop_name, imports_list, type_class_names, serializer_class_names):

        all_of_dict = {
            "serializer_name": prop_name,
            "imports_list": imports_list,
            "type_class_names": type_class_names,
            "serializer_class_names": serializer_class_names
        }
        all_of_file_contents = self.get_all_of_file_contents(all_of_dict)
        all_of_file_path = self.base_path + "/" + prop_name + "Serializer.py"
        from django_swagger_utils.core.utils.write_to_file import write_to_file
        write_to_file(all_of_file_contents, all_of_file_path)

    @staticmethod
    def get_all_of_file_contents(all_of_dict):
        from django_swagger_utils.drf_server.templates.all_of_serializer import ALL_OF_SERIALIZER
        serializer_template = Template(ALL_OF_SERIALIZER)
        context = Context(all_of_dict)
        return serializer_template.render(context)

    def get_object_properties(self, prop_name, schema_properties, options=None):
        if options is None:
            options = []
        serializer_generator = SerializerGenerator(schema_properties=schema_properties,
                                                   base_path=self.base_path,
                                                   serializer_name=prop_name, paths=self.paths)

        context_properties = serializer_generator.generate_serializer_file()
        context_properties["field_string"] = "%s(%s)" % (context_properties["field_string"], ", ".join(options))
        return context_properties

    def get_definition_ref_properties(self, prop_ref, options=None):
        if options is None:
            options = []
        prop_ref_split = prop_ref.split("#/definitions/")
        serializer_name = prop_ref_split[1]
        base_path = self.paths["definitions_serializers_base_dir"]

        from django_swagger_utils.core.utils.convert_path_to_package_str import convert_path_to_package_str
        package_import_str = convert_path_to_package_str(base_path, self.paths['base_dir'])
        base_import_str = "from %s.%s.%sSerializer" % (package_import_str, serializer_name, serializer_name)
        options_str = ", ".join(options)
        context_properties = {"type": "object",
                              "field_string": "%sSerializer(%s)" % (serializer_name, options_str),
                              "serializer_import_str": "%s import %sSerializer" % (base_import_str, serializer_name),
                              "type_file_import_str": "%s import %sType" % (base_import_str, serializer_name),
                              "type_file_class": "%sType" % serializer_name}
        return context_properties

    def get_array_field(self, items, array_name, options, source=None):
        array_context_properties = {
            "serializer_import_str": "",
            "type_file_import_str": "",
            "field_string": "",
            "type": "array"
        }
        items_ref = items.get("$ref", None)
        if not items_ref:
            item_type = items.get("type", None)
            if not items:
                raise Exception("property 'type' not defined for '%s' in '%s' " % (array_name, self.serializer_name))
            if item_type == "integer":
                array_context_properties["field_string"] = "serializers.ListField(child=%s, %s)" % (
                    integer_field(items), ", ".join(options))
            elif item_type == "number":
                array_context_properties["field_string"] = "serializers.ListField(child=%s, %s)" % (
                    number_field(items), ", ".join(options))
            elif item_type == "string":
                array_context_properties["field_string"] = "serializers.ListField(child=%s, %s)" % (
                    string_field(items), ", ".join(options))
            elif item_type == "boolean":
                array_context_properties["field_string"] = "serializers.ListField(child=%s, %s)" % (
                    boolean_field(items), ", ".join(options))
            elif item_type == "array":
                inner_array_items = items.get("items")
                array_context_properties = self.get_array_field(inner_array_items, array_name, options)
                array_context_properties["field_string"] = "serializers.ListField(child=%s, %s)" % (
                    array_context_properties["field_string"], ", ".join(options))
            elif item_type == "object":
                options.append("many=True")
                array_context_properties = self.get_object_properties(array_name, items, options)
                array_context_properties["type"] = "object_array"
            else:
                raise Exception("Type not specified for array object item")
        else:
            options.append("many=True")
            array_context_properties = self.get_definition_ref_properties(items_ref, options)
            array_context_properties["type"] = "object_array"
        return array_context_properties

    def check_field_required(self, prop_name):
        if prop_name in self.required:
            return True
        else:
            return False

    def process_serializer_fields(self):

        field_properties = {}
        optional_params = []
        object_params = {}

        for prop_name, properties in self.fields.iteritems():
            prop_required = self.check_field_required(prop_name)
            if not prop_required:
                if prop_name not in optional_params:
                    optional_params.append(prop_name)

            context_props = self.get_field(prop_name, properties, prop_required)
            field_properties[prop_name] = context_props

            if context_props["type"] == "object" or context_props["type"] == "object_array":
                object_params[prop_name] = context_props
        return field_properties, optional_params, object_params

    def get_serializer_dict(self):

        camel_case_serializer = self.serializer_name

        from django_swagger_utils.core.utils.convert_path_to_package_str import convert_path_to_package_str
        base_import_str = convert_path_to_package_str(self.base_path, self.paths['base_dir'])

        serializer_dict = {
            "serializer_import_str": "from %s.%sSerializer import %sSerializer" % (base_import_str,
                                                                                   camel_case_serializer,
                                                                                   camel_case_serializer),
            "field_string": "%sSerializer" % camel_case_serializer,
            "type_file_import_str": "from %s.%sSerializer import %sType" % (base_import_str, camel_case_serializer,
                                                                            camel_case_serializer),
            "type_file_class": "%sType" % camel_case_serializer,
            "is_array_serializer": self.is_array
        }

        return serializer_dict

    def serializer_file_contents(self, optional_params, field_properties, object_params):

        serializer_context = {
            "required_params": self.required,
            "optional_params": optional_params,
            "params": field_properties,
            "object_params": object_params,
            "serializer_camel_case_name": self.serializer_name
        }

        from django_swagger_utils.drf_server.templates.serializers import SERIALIZERS
        serializer_template = Template(SERIALIZERS)
        context = Context(serializer_context)
        return serializer_template.render(context)

    def write_serializer_file(self, serializer_file_content):
        serializer_file_path = self.base_path + "/" + self.serializer_name + "Serializer.py"

        from django_swagger_utils.core.utils.write_to_file import write_to_file
        write_to_file(serializer_file_content, serializer_file_path)

    def get_list_serializer_file_content(self, field_string):
        from django_swagger_utils.drf_server.templates.list_serializer import LIST_SERIALIZER
        serializer_template = Template(LIST_SERIALIZER)

        context = Context({"field_string": field_string, "serializer_camel_case_name": self.serializer_name})
        return serializer_template.render(context)

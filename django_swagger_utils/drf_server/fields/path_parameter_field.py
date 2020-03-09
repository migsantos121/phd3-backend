def path_param_field(param, parameter_key_name=None, param_name=None):

    if not param_name:
        param_name = param["name"]

    if not parameter_key_name:
        # in case of available parameters, we use the value of parameter name #/parameters/<name>, in other places
        # we are keeping the parameter.name as parameter_key_name
        parameter_key_name = param_name

    from django_swagger_utils.core.utils.case_convertion import to_camel_case
    context_properties = {
        "param_name_camel_case": to_camel_case(param_name),
        "param_name": parameter_key_name,
        "param_field_name": param_name,
        "param_serializer": "",
        "param_serializer_import_str": "",
        "param_serializer_field": "",
        "param_url_regex": "",
        "url_regex": "",
        "example_url_regex": ""
    }
    param_type = param.get("type", None)
    if not param_type:
        raise Exception("property 'type' not defined for form param : %s : %s" % (param_name, parameter_key_name))
    if param_type == "integer":
        url_regex = "\d+"
        example_url_regex = "1234"
    elif param_type == "number":
        url_regex = "\d+(?:\.\d+)?"
        example_url_regex = "12.12"
    elif param_type == "string":
        # single word, no spaces allowed in param name
        url_regex = "\w+"
        example_url_regex = "ibgroup"
    elif param_type == "boolean":
        url_regex = "true|false"
        example_url_regex = "true"
    elif param_type == "array":
        collection_format = param.get("collectionFormat", "csv")

        from django_swagger_utils.drf_server.utils.server_gen.collection_fromat_to_separator import \
            collection_format_to_separator_regex
        separator = collection_format_to_separator_regex(collection_format)
        inner_array_param = param.get("items")
        inner_array_context_properties = path_param_field(inner_array_param, param_name=param_name,
                                                          parameter_key_name=parameter_key_name)
        array_param_regex = inner_array_context_properties["url_regex"]
        array_param_example_regex = inner_array_context_properties["example_url_regex"]
        url_regex = "%s(%s%s)*" % (array_param_regex, separator, array_param_regex)
        example_url_regex = "%s%s%s" % (array_param_example_regex, separator, array_param_example_regex)
    else:
        raise Exception("Invalid value for type of form param")
    context_properties["param_url_regex"] = r"(?P<%s>%s)" % (param_name, url_regex)
    context_properties["url_regex"] = url_regex
    context_properties["example_url_regex"] = example_url_regex
    return context_properties

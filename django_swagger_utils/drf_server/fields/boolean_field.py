def boolean_field(properties, required=True, return_example=False):
    options_list = []

    if not required:
        options_list.append("required=False")

    description = properties.get("description", None)
    if description:
        options_list.append("help_text=\"%s\"" % description)

    default = properties.get("default", None)
    if default:
        options_list.append("default=%s" % default)

    bool_field = 'serializers.BooleanField(%s)' % ", ".join(options_list)

    if return_example:
        default = default if default else True
        return bool_field, default
    return bool_field

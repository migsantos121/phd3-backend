def str_to_snake_case(s):
    import re
    a = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
    return a.sub(r'_\1', s).lower()


def to_camel_case(str_to_convert):
    components = str_to_snake_case(str_to_convert).split('_')
    return components[0].title() + "".join(x.title() for x in components[1:])

def drf_json_parser(json_data_string):
    import ast
    try:
        import json
        json_data_dict = json.loads(json_data_string[1:-1])
        return json_data_dict
    except ValueError:
        json_data_dict = ast.literal_eval(json_data_string)
    from django.utils.six import BytesIO
    from rest_framework.parsers import JSONParser
    stream = BytesIO(json_data_dict)
    data = JSONParser().parse(stream)
    return data

import json

from django.http import HttpResponse
from django.conf import settings

CUSTOM_EXCEPTIONS_DICT = {
    "ValueError": {
        "http_status_code": 400
    },
    "HTTPError": {
        "http_status_code": 400
    },
    "InvalidRequestTypeException": {
        "http_status_code": 400
    },
    "InvalidResponseTypeException": {
        "http_status_code": 400
    },
    "BadRequest": {
        "http_status_code": 400
    },
    "Unauthorized": {
        "http_status_code": 401
    },
    "Forbidden": {
        "http_status_code": 403
    },
    "NotFound": {
        "http_status_code": 404
    },
    "ExpectationFailed": {
        "http_status_code": 417
    }
}


def get_status_code_content(custom_exceptions_list, err, is_json, http_status_code):
    error_class_name = err.__class__.__name__

    exception = custom_exceptions_list[error_class_name]
    is_json = exception.get("is_json", is_json)
    http_status_code = exception.get("http_status_code", http_status_code)

    content = err.message
    res_status = getattr(err, 'res_status', '')
    if is_json:
        try:
            # content = json.loads(content)
            content = json.dumps(content)
        except ValueError:
            pass
    print "Error-Content: ", content
    print "Error-Class: ", error_class_name
    print "Error-Code", http_status_code

    return content, http_status_code, res_status


def get_status_code_content_library(custom_exceptions_list, err, http_status_code):
    error_class_name = err.__class__.__name__

    if error_class_name == "HTTPError":
        content, http_status_code = err.response.content, err.response.status_code
        try:
            return json.loads(content)
        except ValueError:
            return get_data(http_status_code, content)

    exception = custom_exceptions_list[error_class_name]
    http_status_code = exception.get("http_status_code", http_status_code)
    content = err.message
    res_status = getattr(err, 'res_status', '')

    print "Error-Content: ", content
    print "Error-Class: ", error_class_name
    print "Error-Code", http_status_code
    return get_data(http_status_code, content, res_status)


def get_data(http_status_code, content, res_status=''):
    data = {
        "response": content,
        "http_status_code": http_status_code,
        "res_status": res_status
    }
    return data


def handle_custom_exceptions(err):
    error_class_name = err.__class__.__name__
    is_json = False
    http_status_code = 500

    django_swagger_utils_settings = settings.SWAGGER_UTILS
    custom_exceptions_list = django_swagger_utils_settings["CUSTOM_EXCEPTIONS"]

    if error_class_name in custom_exceptions_list.keys():
        content, http_status_code, res_status = get_status_code_content(custom_exceptions_list, err, is_json,
                                                                        http_status_code)
        return HttpResponse(content=content, status=http_status_code)
    elif error_class_name in CUSTOM_EXCEPTIONS_DICT.keys():
        content, http_status_code, res_status = get_status_code_content(CUSTOM_EXCEPTIONS_DICT, err, is_json,
                                                                        http_status_code)
        content = get_data(http_status_code, content, res_status)
        content = json.dumps(content)
        return HttpResponse(content=content, status=http_status_code)
    else:
        raise

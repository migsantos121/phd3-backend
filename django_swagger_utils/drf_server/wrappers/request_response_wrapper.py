import json
import os

from django.conf import settings
from django_swagger_utils.drf_server.utils.decorator.serialize import serialize

from django_swagger_utils.drf_server.utils.decorator.deserialize import deserialize


class RequestResponseWrapper(object):
    def __init__(self, request, options, kwargs):
        self.request = request
        self.options = options
        self.kwargs = kwargs

    def pre_execution(self):

        self.kwargs["user"] = self.request.user
        request_object, request_data = self.request_object_data()
        self.kwargs["request_object"] = request_object
        self.kwargs["request_data"] = request_data
        self.kwargs["request_headers_obj"] = self.request_headers_obj()
        self.kwargs["request_query_params"] = self.request_query_params()

        return self.kwargs

    def post_execution(self, function_return_value):
        response_code, response_obj, response_headers_obj, check_response_serializer = \
            self.get_function_return_val_tuple(function_return_value)
        if check_response_serializer:
            if response_obj is not None:
                function_return_value = response_obj  # if response obj present, default it's return value
                response_serializer, response_headers_serializer, response_many_items = self.check_get_response_data(
                    response_code)

                if response_serializer is not None:
                    response_headers = self.get_response_headers(response_headers_serializer, response_headers_obj)
                    response_headers = self.converted_response_headers(response_headers)
                    function_return_value = self.get_response(response_serializer, response_obj, response_headers,
                                                              response_many_items)
                if isinstance(function_return_value, list):
                    from rest_framework.response import Response
                    function_return_value = Response(data=function_return_value, status=200)
        else:
            function_return_value = response_obj
        return function_return_value

    def check_get_response_data(self, response_code):
        response = self.options["RESPONSE"].get(str(response_code))
        if response:
            response_headers_serializer = response.get("HEADERS_SERIALIZER", None)
            response_serializer = response.get("RESPONSE_SERIALIZER", None)
            response_many_items = response.get("RESPONSE_SERIALIZER_MANY_ITEMS", False)
            return response_serializer, response_headers_serializer, response_many_items
        else:
            from django_swagger_utils.drf_server.exceptions.response_not_definied import ResponseNotDefined
            raise ResponseNotDefined(u'Response for Status Code: {0:s}, Not Defined'.format(response_code))

    @staticmethod
    def get_function_return_val_tuple(function_return_value):
        from rest_framework.response import Response
        from django.http import HttpResponse
        check_response_serializer = True
        if isinstance(function_return_value, tuple):
            if len(function_return_value) == 3:
                response_code = function_return_value[0]
                response_obj = function_return_value[1]
                response_headers_obj = function_return_value[2]

                allowed_primitive_types = [False, str, unicode, int, float]
                # False at 0th index is just for reduce function sake
                if reduce((lambda a, b: a or isinstance(response_obj, b)), allowed_primitive_types):
                    from django.http import HttpResponse
                    response_obj = HttpResponse(str(response_obj))

                if response_obj:
                    if isinstance(response_obj, Response) or isinstance(response_obj, HttpResponse):
                        check_response_serializer = False
                        return None, response_obj, None, check_response_serializer
                    else:
                        return response_code, response_obj, response_headers_obj, check_response_serializer
                elif isinstance(response_obj, list):
                    return response_code, response_obj, response_headers_obj, check_response_serializer
                else:
                    raise Exception("Response object None not allowed")
            else:
                raise Exception("Response Return value Must Be Tuple of 3, (code, response_obj, headers_obj) ")
        elif isinstance(function_return_value, Response) or isinstance(function_return_value, HttpResponse):
            check_response_serializer = False
            return None, function_return_value, None, check_response_serializer
        else:
            raise Exception("Response Return Value must be instance tuple or HTTPResponse or Response")

    @staticmethod
    def get_response_headers(response_headers_serializer, response_headers_obj):
        return serialize(response_headers_serializer, response_headers_obj)

    def get_response(self, response_serializer_class, response_obj, response_headers, response_many_items):
        response_serializer_data = self.serialize_response(response_serializer_class, response_obj, response_many_items)
        from django.conf import settings
        if getattr(settings, 'PRINT_REQUEST_RESPONSE_TO_CONSOLE', None):
            print "Endpoint Response", json.dumps(response_serializer_data, indent=4)

        if os.environ.get("ENCRYPT_RESPONSE", 'FALSE') == 'TRUE':
            print("ENCRYPT_RESPONSE == True ")
            response_serializer_data = {
                "rd": json.dumps(response_serializer_data)
            }
            print(response_serializer_data)

        from rest_framework import status
        from rest_framework.response import Response
        return Response(response_serializer_data, status=status.HTTP_200_OK, headers=response_headers)

    @staticmethod
    def serialize_response(response_serializer_class, response_obj, response_many_items):
        # many = True if isinstance(response_obj, list) else False
        # print response_serializer_class, response_obj, response_many_items

        return serialize(response_serializer_class, response_obj, many=response_many_items)

    def request_object_data(self):
        request_object, request_data = None, None
        if self.options["REQUEST_SERIALIZER"] is not None:
            request_data = self.get_request_data_after_unwrap()
            if getattr(settings, 'PRINT_REQUEST_RESPONSE_TO_CONSOLE', None):
                print "Endpoint Request Data: ", json.dumps(request_data, indent=4)
            request_object = self.get_request_object(data=request_data)

        return request_object, request_data

    def get_request_object(self, data):
        request_serializer_class = self.options["REQUEST_SERIALIZER"]
        partial = self.options["REQUEST_IS_PARTIAL"]
        many = self.options["REQUEST_SERIALIZER_MANY_ITEMS"]
        return deserialize(request_serializer_class, data, partial=partial, many=many)

    def get_request_data_after_unwrap(self):
        if self.options['REQUEST_WRAPPING_REQUIRED']:
            data = self.wrapped_request_data()
        else:
            data = self.get_request_data()
        return data

    def get_request_data(self):
        data = self.request.data
        if self.request.method == 'GET':
            if not data:
                data = self.request.query_params
        return data

    def wrapped_request_data(self):
        wrapper_request_object = self.get_wrapper_request_object()
        if self.options["REQUEST_ENCRYPTION_REQUIRED"]:

            from django_swagger_utils.drf_server.utils.decorator.encrypt_request_data import encrypt_request_data
            json_data_string = encrypt_request_data(wrapper_request_object)
        else:
            json_data_string = wrapper_request_object.data

        from django_swagger_utils.drf_server.utils.decorator.drf_json_parser import drf_json_parser
        data = drf_json_parser(json_data_string)
        return data

    def get_wrapper_request_object(self):
        data = self.get_request_data()
        from django_swagger_utils.drf_server.serializers.base_request.baseRequestSerializer import BaseRequestSerializer
        return deserialize(BaseRequestSerializer, data)

    def request_headers_obj(self):
        request_headers_serializer = self.options.get("REQUEST_HEADERS_SERIALIZER", None)
        return deserialize(request_headers_serializer, self.request.META)

    def request_query_params(self):
        request_query_params_serializer = self.options.get("REQUEST_QUERY_PARAMS_SERIALIZER", None)
        return deserialize(request_query_params_serializer, self.request.query_params)

    @staticmethod
    def converted_response_headers(response_headers):
        _dict = {}
        if response_headers:
            for header_name, header_value in response_headers.iteritems():
                header_name = header_name.replace("_", "-")
                _dict[header_name] = header_value
        return _dict

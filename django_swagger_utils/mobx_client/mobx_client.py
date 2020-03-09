from django.template.base import Template
from django.template.context import Context

from django_swagger_utils.core.utils.write_to_file import write_to_file

__author__ = 'tanmay.ibhubs'

import re
import os


class MobxTemplateGenerator:
    def __init__(self, parser, app_name, mobx_base_dir):
        '''
        parser to parse the spec file and appname to store the files are required.
        :param parser:
        :param appname:
        '''
        self.parser = parser
        self.app_name = app_name
        self.mobx_base_dir = mobx_base_dir
        self.primitive_types = ('integer', 'string', 'boolean', 'number')

    def convert_to_snake(self, name):
        '''
        convert name from camelCase to snake_case
        :param name:
        :return:
        '''
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def get_camel(self, column):
        '''
        convert column from snake_case to camelCase
        :param column:
        :return:
        '''
        words = column.split('_')
        first = words[0]
        return first + ''.join((w.capitalize() for w in words[1:]))

    def get_capitalized(self, column):
        '''
        convert column from snake_case to camelCase
        :param column:
        :return:
        '''
        words = column.split('_')
        words = [(w[0].capitalize() + w[1:]) for w in words]
        return ''.join(words)

    def get_camel_from_capitalized(self, capitalized):
        return capitalized[0].lower() + capitalized[1:]

    def get_self_item(self, each_property, context_dict):
        '''
        This method is being used for the constructor field.
        If the type is array , we just need 'observable([])' to print in the constructor field
        :param each_property:
        :param context_dict:
        :return:
        '''
        if context_dict['flag']:
            context_dict['flag'] = False
            return 'observable([])'
        else:
            return each_property

    def get_default(self, type, property_def, result):
        '''
        This methods is being used to get the default value of any type so as to be used in mobx-classes
        :param type: ->type of which we need to get the default value
        :param property_def: -> in classes it is of complex type like array or object , we need to get its default for
        the mobx class
        :param result:-> specially being used for recursion, in case of array and object
        :return:
        '''
        if type != None:
            if type == 'boolean':
                return True
            elif type == 'integer':
                return -1
            elif type == 'number':
                return -1
            elif type == 'string':
                return "\"\""
            elif type == 'array':
                items = property_def.get('items')
                result = '[' + str(self.get_default(items.get('type'), items, result)) + ']'
                return result
            elif type == 'object':
                return ''
            else:
                return ''

    def generate_definitions(self, base_path):
        '''
        This is the driver program which generates definitions.
        :return:
        '''
        for def_name, definition in self.parser.definitions().iteritems():
            self.generate_definition(model_name=def_name, body=definition, base_path=base_path)

            # if not isinstance(data, type(None)):
            #     write_path = os.path.join(base_path, def_name, 'index' + '.js')
            #     write_to_file(data, write_path, False)

    def generate_definition(self, **kwargs):
        model_name = kwargs['model_name']
        kwargs['extra_imports'] = ''
        kwargs['api_type_import'] = "API" + model_name
        kwargs['capital_name'] = self.get_capitalized(model_name)
        kwargs['camel_name'] = self.get_camel_from_capitalized(model_name)
        kwargs['import_flag'] = False
        kwargs['flag'] = False
        kwargs['fields'] = []
        kwargs['constructor'] = []
        kwargs['actions'] = []
        kwargs['api_model_dict'] = {}
        kwargs['api_model_dict']['import'] = ''
        kwargs['api_model_dict']['class_name'] = 'API' + self.get_capitalized(model_name)
        kwargs['api_model_dict']['fields'] = []
        kwargs['request_data'] = []
        if 'to_write' not in kwargs:
            kwargs['to_write'] = True
        if 'allOf' in kwargs['body']:
            kwargs = self.generate_all_of_definition(**kwargs)
        elif kwargs['body']['type'] == 'object':
            kwargs = self.generate_object_definition(**kwargs)
        elif kwargs['body']['type'] == 'array':
            kwargs = self.generate_array_definition(**kwargs)

        if kwargs['to_write']:
            if 'from_endpoint' in kwargs and kwargs['from_endpoint']:
                from django_swagger_utils.mobx_client.templates.mobx_apimodel import apimodel
                api_template = Template(apimodel)
                write_path = os.path.join(kwargs['base_path'], model_name, kwargs['endpoint_type'], 'type.js')
                write_to_file(api_template.render(Context(kwargs['api_model_dict'])), write_path,
                              False)

                from django_swagger_utils.mobx_client.templates.mobx_models import models
                mobx_template = Template(models)
                mobx_template.render(Context(kwargs))
                write_path = os.path.join(kwargs['base_path'], model_name, kwargs['endpoint_type'], 'index.js')
                write_to_file(mobx_template.render(Context(kwargs)), write_path,
                              False)
            else:
                from django_swagger_utils.mobx_client.templates.mobx_apimodel import apimodel
                api_template = Template(apimodel)
                write_path = os.path.join(kwargs['base_path'], model_name, 'type.js')
                write_to_file(api_template.render(Context(kwargs['api_model_dict'])), write_path,
                              False)

                from django_swagger_utils.mobx_client.templates.mobx_models import models
                mobx_template = Template(models)
                mobx_template.render(Context(kwargs))
                write_path = os.path.join(kwargs['base_path'], model_name, 'index.js')
                write_to_file(mobx_template.render(Context(kwargs)), write_path,
                              False)

        return kwargs

    def generate_object_definition(self, **kwargs):
        properties = kwargs['body'].get('properties', {})
        model_name = kwargs['model_name']
        for each_property in properties.keys():
            property_def = properties[each_property]

            if '$ref' in property_def:
                ref_name = property_def['$ref']
                reference_def = ref_name.split('/')[2]
                ex_import = 'import ' + reference_def + ' from \'../' + reference_def + '/' + 'index.js\'\n'
                ex_api_import = 'import type {API' + self.get_capitalized(
                    reference_def) + '} from \'../' + reference_def + '/type.js\'\n'

                if ex_import not in kwargs['extra_imports']:
                    kwargs['extra_imports'] += ex_import
                if ex_api_import not in kwargs['api_model_dict']['import']:
                    kwargs['api_model_dict']['import'] += ex_api_import

                field = (each_property, reference_def)
                request_data_field = (each_property, 'object')
                api_type_field = (each_property, "API" + reference_def)
                constructor = (self.get_camel(each_property),
                               "new " + self.get_capitalized(
                                   reference_def) + "(" + self.get_camel_from_capitalized(
                                   model_name) + "." + each_property + ")",
                               '')

                action = (self.get_capitalized(each_property), self.get_camel(each_property),
                          ":" + self.get_capitalized(reference_def), '=' + '{}',
                          "new " + self.get_capitalized(reference_def) + '(' + self.get_camel(
                              each_property) + ')')
                kwargs['fields'].append(field)
                kwargs['request_data'].append(request_data_field)
                kwargs['actions'].append(action)
                kwargs['constructor'].append(constructor)
                kwargs['api_model_dict']['fields'].append(api_type_field)


            elif 'type' in property_def:
                prop_type = property_def['type']

                if prop_type in self.primitive_types:
                    if prop_type == 'integer':
                        prop_type = 'number'
                    field = (each_property, prop_type)
                    default_type = self.get_default(prop_type, property_def, '')
                    constructor = (
                        self.get_camel(each_property),
                        self.get_self_item(each_property, kwargs),
                        '||' + str(default_type))
                    action = (self.get_capitalized(each_property),
                              self.get_camel(each_property), ':' + str(prop_type), '=' + str(default_type),
                              self.get_camel(each_property))
                    kwargs['fields'].append(field)
                    kwargs['request_data'].append(field)
                    kwargs['actions'].append(action)
                    kwargs['constructor'].append(constructor)
                    kwargs['api_model_dict']['fields'].append(field)
                elif prop_type == 'object':
                    self.generate_definition(model_name=self.get_capitalized(each_property), body=property_def,
                                             base_path=kwargs['base_path'] + "/" + model_name)

                    kwargs[
                        'extra_imports'] += 'import ' + self.get_capitalized(
                        each_property) + ' from \'./' + self.get_capitalized(each_property) + '/' + 'index.js\'\n'
                    kwargs['api_model_dict']['import'] += 'import type {API' + self.get_capitalized(
                        each_property) + '} from \'./' + self.get_capitalized(each_property) + '/type.js\'\n'

                    field = (each_property, self.get_capitalized(each_property))
                    request_data_field = (each_property, 'object')
                    api_type_field = (each_property, "API" + self.get_capitalized(each_property))
                    constructor = (self.get_camel(each_property),
                                   "new " + self.get_capitalized(each_property) + "(" + self.get_camel_from_capitalized(
                                       model_name) + "." + each_property + ")",
                                   '')

                    action = (self.get_capitalized(each_property), self.get_camel(each_property),
                              ":" + self.get_capitalized(each_property), '=' + '{}',
                              "new " + self.get_capitalized(each_property) + '(' + self.get_camel(
                                  each_property) + ')')

                    kwargs['fields'].append(field)
                    kwargs['request_data'].append(request_data_field)
                    kwargs['actions'].append(action)
                    kwargs['constructor'].append(constructor)
                    kwargs['api_model_dict']['fields'].append(api_type_field)
                elif prop_type == 'array':
                    v_kwargs = self.generate_definition(
                        model_name=each_property, body=property_def,
                        base_path=kwargs['base_path'] + "/" + self.get_capitalized(model_name))

                    kwargs['fields'].extend(v_kwargs['fields'])
                    kwargs['request_data'].extend(v_kwargs['request_data'])
                    kwargs['actions'].extend(v_kwargs['actions'])
                    kwargs['constructor'].extend(v_kwargs['constructor'])
                    kwargs['api_model_dict']['fields'].extend(v_kwargs['api_model_dict']['fields'])
                    kwargs['extra_imports'] += v_kwargs['extra_imports']
                    kwargs['api_model_dict']['import'] += v_kwargs['api_model_dict']['import']
                    kwargs['import_flag'] = True
                    kwargs['api_model_dict']['import_flag'] = True

            elif 'allOf' in property_def:

                self.generate_definition(model_name=self.get_capitalized(each_property), body=property_def,
                                         base_path=kwargs['base_path'] + "/" + model_name)

                ex_import = 'import ' + self.get_capitalized(
                    each_property) + ' from \'./' + self.get_capitalized(each_property) + '/' + 'index.js\'\n'
                ex_api_import = 'import type {API' + self.get_capitalized(
                    each_property) + '} from \'./' + self.get_capitalized(each_property) + '/type.js\'\n'

                if ex_import not in kwargs['extra_imports']:
                    kwargs['extra_imports'] += ex_import
                if ex_api_import not in kwargs['api_model_dict']['import']:
                    kwargs['api_model_dict']['import'] += ex_api_import

                field = (each_property, self.get_capitalized(each_property))
                request_data_field = (each_property, 'object')
                api_type_field = (each_property, "API" + self.get_capitalized(each_property))
                constructor = (self.get_camel(each_property),
                               "new " + self.get_capitalized(each_property) + "(" + self.get_camel_from_capitalized(
                                   model_name) + "." + each_property + ")",
                               '')

                action = (self.get_capitalized(each_property), self.get_camel(each_property),
                          ":" + self.get_capitalized(each_property), '=' + '{}',
                          "new " + self.get_capitalized(each_property) + '(' + self.get_camel(
                              each_property) + ')')

                kwargs['fields'].append(field)
                kwargs['request_data'].append(request_data_field)
                kwargs['actions'].append(action)
                kwargs['constructor'].append(constructor)
                kwargs['api_model_dict']['fields'].append(api_type_field)

        return kwargs

    def generate_array_definition(self, **kwargs):
        model_name = kwargs['model_name']
        items = kwargs['body']['items']
        prop_result = 'IObservableArray'
        api_prop_result = prop_result
        default_type = 'observable([])'

        if 'type' in items:
            prop_type = items['type']
            if prop_type in self.primitive_types:
                kwargs['to_write'] = False
                if prop_type == 'integer':
                    prop_type = 'number'
                prop_result += '<' + prop_type + '>'
                field = (model_name, prop_result)

                constructor = (
                    self.get_camel(model_name),
                    model_name,
                    '||' + str(default_type))
                action = (self.get_capitalized(model_name),
                          self.get_camel(model_name), ':' + str(prop_result), '=' + str(default_type),
                          self.get_camel(model_name))

                api_type_field = (model_name, prop_result)
                kwargs['fields'].append(field)
                kwargs['request_data'].append(field)
                kwargs['actions'].append(action)
                kwargs['constructor'].append(constructor)
                kwargs['api_model_dict']['fields'].append(api_type_field)

            elif prop_type == 'object':
                kwargs = self.generate_definition(model_name=self.get_capitalized(model_name), body=items,
                                                  base_path=kwargs['base_path'])

                kwargs['to_write'] = False

                ex_import = 'import ' + self.get_capitalized(
                    model_name) + ' from \'../' + self.get_capitalized(model_name) + '/' + 'index.js\'\n'
                ex_api_import = 'import type {API' + self.get_capitalized(
                    model_name) + '} from \'../' + self.get_capitalized(model_name) + '/type.js\'\n'

                if ex_import not in kwargs['extra_imports']:
                    kwargs['extra_imports'] += ex_import
                if ex_api_import not in kwargs['api_model_dict']['import']:
                    kwargs['api_model_dict']['import'] += ex_api_import

                prop_result += '<' + self.get_capitalized(model_name) + '>'
                api_prop_result += '<' + 'API' + self.get_capitalized(model_name) + '>'

                field = (model_name, prop_result)

                api_type_field = (model_name, api_prop_result)
                constructor = (
                    self.get_camel(model_name),
                    model_name,
                    '||' + str(default_type))
                action = (self.get_capitalized(model_name),
                          self.get_camel(model_name), ':' + str(prop_result), '=' + str(default_type),
                          self.get_camel(model_name))
                kwargs['fields'] = [field]
                kwargs['actions'] = [action]
                kwargs['request_data'].append(field)
                kwargs['constructor'] = [constructor]
                kwargs['api_model_dict']['fields'] = [api_type_field]

        if '$ref' in items:
            ref_name = items['$ref']
            prop_type = ref_name.split('/')[2]
            prop_result += '<' + prop_type + '>'
            api_prop_result += '<' + 'API' + prop_type + '>'
            field = (model_name, prop_result)
            kwargs['to_write'] = False
            ex_import = 'import ' + prop_type + ' from \'../' + prop_type + '/' + 'index.js\'\n'
            ex_api_import = 'import type {API' + prop_type + '} from \'../' + prop_type + '/type.js\'\n'

            if ex_import not in kwargs['extra_imports']:
                kwargs['extra_imports'] += ex_import
            if ex_api_import not in kwargs['api_model_dict']['import']:
                kwargs['api_model_dict']['import'] += ex_api_import

            constructor = (
                self.get_camel(model_name),
                model_name,
                '||' + str(default_type))
            action = (self.get_capitalized(model_name),
                      self.get_camel(model_name), ':' + str(prop_result), '=' + str(default_type),
                      self.get_camel(model_name))

            api_type_field = (model_name, api_prop_result)
            kwargs['fields'].append(field)
            kwargs['request_data'].append(field)
            kwargs['actions'].append(action)
            kwargs['constructor'].append(constructor)
            kwargs['api_model_dict']['fields'].append(api_type_field)

        elif 'allOf' in items:
            self.generate_definition(model_name=self.get_capitalized(model_name), body=items,
                                     base_path=kwargs['base_path'])
            kwargs['to_write'] = False
            ex_import = 'import ' + self.get_capitalized(
                model_name) + ' from \'../' + self.get_capitalized(model_name) + '/' + 'index.js\'\n'
            ex_api_import = 'import type {API' + self.get_capitalized(
                model_name) + '} from \'../' + self.get_capitalized(model_name) + '/type.js\'\n'

            if ex_import not in kwargs['extra_imports']:
                kwargs['extra_imports'] += ex_import
            if ex_api_import not in kwargs['api_model_dict']['import']:
                kwargs['api_model_dict']['import'] += ex_api_import

            prop_result += '<' + self.get_capitalized(model_name) + '>'

            api_prop_result += '<' + 'API' + self.get_capitalized(model_name) + '>'

            field = (model_name, prop_result)
            kwargs['to_write'] = False
            constructor = (
                self.get_camel(model_name),
                model_name,
                '||' + str(default_type))
            action = (self.get_capitalized(model_name),
                      self.get_camel(model_name), ':' + str(prop_result), '=' + str(default_type),
                      self.get_camel(model_name))

            api_type_field = (model_name, api_prop_result)
            kwargs['fields'].append(field)
            kwargs['request_data'].append(field)
            kwargs['actions'].append(action)
            kwargs['constructor'].append(constructor)
            kwargs['api_model_dict']['fields'].append(api_type_field)

        return kwargs

    def generate_all_of_definition(self, **kwargs):
        model_name = kwargs['model_name']
        allOf = kwargs['body']['allOf']
        for each_ref in allOf:
            if '$ref' in each_ref:
                name = each_ref.get('$ref')
                name = name.split('/')[2]
                for v_def_name, v_definition in self.parser.definitions().iteritems():
                    if name == v_def_name:
                        v_kwargs = self.generate_definition(model_name=self.get_capitalized(model_name),
                                                            body=v_definition,
                                                            base_path=kwargs['base_path'])

                        kwargs['fields'].extend(v_kwargs['fields'])
                        kwargs['request_data'].extend(v_kwargs['request_data'])
                        kwargs['actions'].extend(v_kwargs['actions'])
                        kwargs['constructor'].extend(v_kwargs['constructor'])
                        kwargs['api_model_dict']['fields'].extend(v_kwargs['api_model_dict']['fields'])
                        if v_kwargs['extra_imports'] not in kwargs['extra_imports']:
                            kwargs['extra_imports'] += v_kwargs['extra_imports']
                        if v_kwargs['api_model_dict']['import'] not in kwargs['api_model_dict']['import']:
                            kwargs['api_model_dict']['import'] += v_kwargs['api_model_dict']['import']

                        kwargs['import_flag'] = True
                        kwargs['api_model_dict']['import_flag'] = True
            elif 'type' in each_ref:
                if each_ref['type'] == 'object':
                    v_kwargs = self.generate_definition(model_name=self.get_capitalized(model_name), body=each_ref,
                                                        base_path=kwargs['base_path'], to_write=False)

                    kwargs['fields'].extend(v_kwargs['fields'])
                    kwargs['request_data'].extend(v_kwargs['request_data'])
                    kwargs['actions'].extend(v_kwargs['actions'])
                    kwargs['constructor'].extend(v_kwargs['constructor'])
                    kwargs['api_model_dict']['fields'].extend(v_kwargs['api_model_dict']['fields'])
                    if v_kwargs['extra_imports'] not in kwargs['extra_imports']:
                        kwargs['extra_imports'] += v_kwargs['extra_imports']
                    if v_kwargs['api_model_dict']['import'] not in kwargs['api_model_dict']['import']:
                        kwargs['api_model_dict']['import'] += v_kwargs['api_model_dict']['import']

                    kwargs['import_flag'] = True
                    kwargs['api_model_dict']['import_flag'] = True

        return kwargs

    def generate_parameters(self, base_path):
        for parameter_name, parameter_body in self.parser.parameters().iteritems():
            schema = parameter_body.get('schema', None)
            if not schema:
                return

            elif '$ref' in schema:
                return

            elif schema.get('type', None) == 'object':
                self.generate_definition(model_name=parameter_name, body=schema,
                                         base_path=base_path)

    def generate_responses(self, base_path):
        for response_name, response_body in self.parser.responses().iteritems():
            if '$ref' in response_body:
                continue
            schema = response_body.get('schema')
            if not schema:
                return

            elif '$ref' in schema:
                return

            elif schema.get('type', None) == 'object':
                self.generate_definition(model_name=response_name, body=schema,
                                         base_path=base_path)

    def generate_endpoints(self, base_path):
        for path, path_body in self.parser.paths().iteritems():
            for each_method in path_body.keys():
                if each_method in ['get', 'put', 'delete', 'post', 'update']:
                    inner_body = path_body[each_method]
                    operation_id = inner_body['operationId']

                    # form responses
                    responses = inner_body['responses']
                    responses = responses['200']
                    response_name = self.get_capitalized(operation_id)
                    if '$ref' in responses:
                        continue
                    schema = responses.get('schema', None)
                    if schema is None:
                        continue
                    elif '$ref' in schema:
                        continue
                    elif schema.get('type') == 'object':
                        self.generate_definition(model_name=response_name, body=schema,
                                                 base_path=base_path, from_endpoint=True, endpoint_type='response')

                    # form parameters
                    parameters = inner_body.get('parameters', None)
                    if not parameters:
                        continue

                    for parameter in parameters:
                        parameter_name = self.get_capitalized(operation_id)
                        schema = parameter.get('schema', None)
                        if not schema:
                            return
                        if schema is None:
                            return
                        if '$ref' in schema:
                            return

                        if schema.get('type') == 'object':
                            self.generate_definition(model_name=parameter_name, body=schema,
                                                     base_path=base_path, from_endpoint=True, endpoint_type='request')

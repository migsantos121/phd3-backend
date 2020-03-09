import importlib
import json
import os

from django.template import Template, Context

from django_swagger_utils.core.utils.write_to_file import write_to_file

from django_swagger_utils.core.utils.case_convertion import to_camel_case


class InterfaceGenerator:
    def __init__(self, appname, parser, interface_dir):
        self.app_name = appname
        self.parser = parser
        self.interface_dir = interface_dir
        self.interface_not_required = []

    def get_required_interface_feilds(self):
        """
        in the spec file , we have included a x-interface-required field,
        by default this feild is true,
        if we explicitly mention it as false , interface for that api wont be generated
        :return:
        """
        for path, path_body in self.parser.paths().iteritems():
            for each_method in path_body.keys():
                if each_method in ['get', 'put', 'delete', 'post', 'update']:
                    inner_body = path_body[each_method]
                    interface_required = inner_body.get("x-interface-required")
                    if interface_required == None:
                        continue
                    elif interface_required == False:
                        self.interface_not_required.append(inner_body.get('operationId'))
                        # print self.interface_not_required

    def get_immediate_subdirectories(self, current_dir):
        '''
        Being used to get immediate subdirectories of a directory
        :param current_dir:
        :return:
        '''
        return [name for name in os.listdir(current_dir)
                if os.path.isdir(current_dir + '/' + name)]

    def generate_interfaces(self):
        '''
        driver method.
        calls other methods to generate the interfaces.
        :return:
        '''
        self.get_required_interface_feilds()
        # ****UNCOMMENT THE BELOW LINE FOR VALIDATION THROUGH SERILIZER ALSO****
        # self.get_validator_data()
        from django_swagger_utils.core.utils.check_path_exists import check_path_exists
        base_path = self.interface_dir
        if not check_path_exists(os.path.join(base_path, self.app_name + "_service_interface.py")):
            context_dict = {}
            context_dict['app_name_capital'] = to_camel_case(self.app_name.capitalize())
            context_dict['app_name_upper'] = self.app_name.upper()
            context_dict['app_name'] = self.app_name
            context_dict['author'] = 'iB'
            function_list = []
            for path, path_body in self.parser.paths().iteritems():
                for each_method in path_body.keys():
                    if each_method in ['get', 'put', 'delete', 'post', 'update']:
                        inner_body = path_body[each_method]
                        operation_id = inner_body['operationId']
                        if operation_id in self.interface_not_required:
                            continue
                        # ****UNCOMMENT THE BELOW LINES FOR VALIDATION THROUGH SERILIZER ALSO****
                        # serial_import = self.serilizer_import[operation_id]
                        # if serial_import == ' ':
                        #     import_flag = False
                        #     serializer_name = ' '
                        # else:
                        #     import_flag = True
                        #     serializer_name = serial_import.split('import')[1]
                        #     serializer_name = serializer_name[1:]
                        functions = (
                            operation_id, each_method.upper(), path)
                        function_list.append(functions)
            context_dict['functions'] = function_list
            from django_swagger_utils.interface_client.templates.interface_template import interface_template
            template = Template(interface_template)
            data = template.render(Context(context_dict))
            write_to_file(data, os.path.join(base_path, self.app_name + "_service_interface.py"))

            # ****UNCOMMENT THE BELOW LINES FOR VALIDATION THROUGH SERIALIZER ALSO****
            # def get_validator_data(self):
            #     self.serilizer_import = {}
            #     view_environment_path = self.appname + "/build/view_environments/"
            #     path_subdirectories = self.get_immediate_subdirectories(view_environment_path)
            #     import_str1 = self.appname + '.build.view_environments'
            #     for each_path in path_subdirectories:
            #         combined_path1 = view_environment_path + '/' + each_path
            #         import_str2 = import_str1 + '.' + each_path
            #         action_subdirectories = self.get_immediate_subdirectories(combined_path1)
            #         for each_action in action_subdirectories:
            #             import_str3 = import_str2 + '.' + each_action + '.' + each_action
            #             combined_path2 = combined_path1 + '/' + each_action + "/" + each_action + ".py"
            #             self.get_serializer_import(import_str3, combined_path2, each_action)

            # def get_serializer_import(self, path, libname, operation_id):
            #     options = getattr(importlib.import_module(path), 'options')
            #     if options['REQUEST_SERIALIZER'] == None:
            #         self.serilizer_import[operation_id] = ' '
            #     else:
            #         file = open(libname, 'r')
            #         for each_line in file.readlines():
            #             if each_line.startswith("from " + self.appname):
            #                 self.serilizer_import[operation_id] = each_line
            #                 break

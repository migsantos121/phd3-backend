import json

from django.template import Template, Context


class URLGenerator(object):
    context_properties = None

    def __init__(self, app_name, dir_paths, parser):
        self.app_name = app_name
        self.dir_paths = dir_paths
        self.parser = parser

    def configure(self):
        self.set_context_properties()

    def set_context_properties(self):
        self.context_properties = self.get_url_context_properties()

    def generate_url(self):
        url_file_contents = self.get_url_file_contents(self.context_properties)
        url_path = self.dir_paths["url_file"]

        from django_swagger_utils.core.utils.write_to_file import write_to_file
        write_to_file(url_file_contents, url_path)

    def generate_view_environment(self):

        for url_path, path_properties in self.context_properties.iteritems():
            path_method_dict_str = json.dumps(path_properties["path_method_dict"], indent=4)
            context_properties = {
                "path_method_dict_str": path_method_dict_str,
                "path_method_name": path_properties["view_environment"]["path_name"],
                "app_name": self.app_name
            }
            view_environment_file_contents = self.get_view_environment_router_file_contents(context_properties)
            view_environment_file_path = path_properties["view_environment"]["view_environment_router_path"]
            
            from django_swagger_utils.core.utils.write_to_file import write_to_file
            write_to_file(view_environment_file_contents, view_environment_file_path)

    def get_url_context_properties(self):
        context_properties = {}
        all_method_operation_ids = []
        for path_name, path in self.parser.paths().iteritems():
            from django_swagger_utils.drf_server.generators.path_generator import PathGenerator
            path_generator = PathGenerator(self.app_name, self.dir_paths, path, path_name, self.parser)
            path_method_dict, view_environment_path_dict, operation_ids = path_generator.get_urls()
            all_method_operation_ids.extend(operation_ids)

            context_properties[path_name] = {
                "path_method_dict": path_method_dict,
                "view_environment": view_environment_path_dict
            }

        return context_properties

    @staticmethod
    def get_url_file_contents(context_properties):

        from django_swagger_utils.drf_server.templates.urls import URL
        serializer_template = Template(URL)
        context = Context({"path_names": context_properties})
        return serializer_template.render(context)

    @staticmethod
    def get_view_environment_router_file_contents(context_properties):

        from django_swagger_utils.drf_server.templates.router import ROUTER
        serializer_template = Template(ROUTER)
        context = Context(context_properties)
        return serializer_template.render(context)


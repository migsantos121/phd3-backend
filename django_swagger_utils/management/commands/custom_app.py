import os

from django.core.management.base import BaseCommand


class CreateCustomApp(object):
    def __init__(self, app_name, base_path):
        self.app_name = app_name
        self.base_path = base_path

    def create_app(self):
        """
        creates new app
        :return:
        """
        app_base_path = os.path.join(self.base_path, self.app_name)
        from django_swagger_utils.core.utils.check_path_exists import check_path_exists
        #if app is present already
        if check_path_exists(app_base_path):
            print u"'{0:s}' already exists".format(self.app_name)
            exit()
        else:
            #write all default file
            folders_list, files_list = self.get_default_files_list()
            for each_file in files_list.values():
                from django_swagger_utils.core.utils.write_to_file import write_to_file
                write_to_file(each_file[1], each_file[0])
            from django_swagger_utils.drf_server.utils.server_gen.get_api_environment import  check_to_execute_mock_tests_for_apps
            from django_swagger_utils.core.utils.write_to_file import write_to_file

            view_file_init_file_path=self.base_path+"/"+self.app_name+"/__init__.py"
            view_init_file_contents="EXECUTE_API_TEST_CASE = "+ str(check_to_execute_mock_tests_for_apps(self.app_name))
            write_to_file(view_init_file_contents, view_file_init_file_path)
            for each_folder in folders_list.values():
                from django_swagger_utils.core.utils.mk_dirs import MkDirs
                MkDirs().mk_dir_if_not_exits(file_name=each_folder)
        print u"'{0:s}' created".format(self.app_name)
        os.system("tree {0:s}".format(self.app_name))

        # todo: updated swagger_utils settings.apps

    def get_default_files_list(self):
        #creates path for default files and returns folders and files dict
        app_base_path = os.path.join(self.base_path, self.app_name)
        api_specs_dir = os.path.join(app_base_path, 'api_specs')
        conf_dir = os.path.join(app_base_path, 'conf')

        sample_api_specs_json = self.get_sample_api_specs_json()
        files_list = {
            "api_spec_json": (
                os.path.join(api_specs_dir, 'api_spec.json'), sample_api_specs_json),
            "settings_file": (os.path.join(conf_dir, 'settings.py'), "# write your %s settings" % self.app_name),
        }

        folders_list = {
            # "use_cases_dir": os.path.join(conf_dir, 'use_cases/'),
            # "responses_dir": os.path.join(conf_dir, 'responses/')
        }

        return folders_list, files_list

    def get_sample_api_specs_json(self):
        """
        returns a sample spec
        :return:
        """
        from django_swagger_utils.drf_server.utils.server_gen.sample_spec_file import sample_spec_file
        sample_specs_json = sample_spec_file(self.app_name)
        return sample_specs_json


class Command(BaseCommand):
    can_import_settings = True
    help = 'Generate a custom swagger util template app'

    def add_arguments(self, parser):
        """
        retrieve each argument seperated by white space where each of them represent an app
        nargs=* indicates atleast 1 argument to be present
        to know more about arguments and nargs read the python documentaion
        :param parser:
        :return:
        """
        parser.add_argument('app', nargs='*', type=str, help="list of apps")

    def handle(self, *args, **options):
        from django.conf import settings
        base_dir = settings.BASE_DIR
        try:
            apps = options['app']
            if not apps:
                print "usage: python manage.py custom_app <app_names> "
                exit()
            for app_name in apps:
                create_custom_app = CreateCustomApp(app_name, base_dir)
                create_custom_app.create_app()
        except Exception, err:
            print err
            exit(1)
            raise

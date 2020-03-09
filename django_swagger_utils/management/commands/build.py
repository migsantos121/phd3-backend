import json
import os
import shutil
import subprocess

from django.core.management.base import BaseCommand, CommandError


class Build(object):
    spec_json = None
    parser = None
    paths = dict()

    def __init__(self, app_name, base_dir, settings=None):
        self.app_name = app_name
        self.base_dir = base_dir
        self.settings = settings
        self.initiate_build()

    def initiate_build(self):
        # setup build specific paths
        self.setup_paths()

        # create settings file if not exists
        self.check_create_settings_file()

        # step1 check build dir exists
        # self.check_build_exists()

        # step2 load api_spec.json into spec_json
        self.load_spec_file(self.paths["api_specs_json"])

        # step3 validate specs_json
        self.validate_swagger()

        # step4 custom spec validation
        self.custom_spec_validator()

        # step5 parser swagger specs
        self.parse_swagger_specs()

    def setup_paths(self):
        """
        defines paths used in the project
        :return:
        """
        # TODO: separate out paths based on android, json patch, server_gen.
        app_base_path = os.path.join(self.base_dir, self.app_name)
        build_dir = os.path.join(app_base_path, "build")
        api_spec_dir = os.path.join(app_base_path, "api_specs")
        api_spec_migrations_dir = os.path.join(api_spec_dir, "migrations")
        api_specs_json = os.path.join(api_spec_dir, "api_spec.json")
        request_response_dir = os.path.join(build_dir, "request_response")
        decorator_options_file = os.path.join(request_response_dir, "decorator_options.py")
        security_definitions_file = os.path.join(request_response_dir, "security_definitions.py")
        serializers_base_dir = os.path.join(build_dir, "serializers")
        definitions_serializers_base_dir = os.path.join(serializers_base_dir, "definitions")
        global_parameters_dir = os.path.join(build_dir, "parameters")
        global_response_dir = os.path.join(build_dir, "responses")
        url_file = os.path.join(build_dir, "urls.py")
        mobx_base_dir = os.path.join(build_dir, "mobx_classes")
        mobx_base_dir_models = os.path.join(mobx_base_dir, 'models')
        mobx_base_dir_responses = os.path.join(mobx_base_dir, 'responses')
        mobx_base_dir_endpoints = os.path.join(mobx_base_dir, 'endpoints')
        mobx_base_dir_parameters = os.path.join(mobx_base_dir, 'parameters')
        view_environments_dir = os.path.join(build_dir, "view_environments")
        sample_json_dir = os.path.join(app_base_path, "conf", "responses")
        settings_file = os.path.join(app_base_path, "conf", "settings.py")
        mock_views_dir = os.path.join(build_dir, "mock_views")
        views_dir = os.path.join(app_base_path, "views")
        api_environment_file = os.path.join(api_spec_dir, "api_environment.py")
        android_base_dir = os.path.join(build_dir, "android_%s" % self.app_name)
        api_doc_dir = os.path.join(build_dir, "docs")
        tests_dir = os.path.join(app_base_path, "tests")
        global_jars_dir = os.path.join(self.base_dir, "android_jars")
        zappa_settings = os.path.join(self.base_dir, "zappa_settings.json")
        apidoc = os.path.join(self.base_dir, "apidoc.json")
        docs = os.path.join(self.base_dir, "docs")
        static = os.path.join(self.base_dir, "static")
        static_docs = os.path.join(static, "docs")
        interface_dir = os.path.join(app_base_path, 'interfaces')
        package_json = os.path.join(self.base_dir, "package.json")
        self.paths = {
            "base_dir": self.base_dir,
            "app_base_path": app_base_path,
            "build_dir": build_dir,
            "api_spec_dir": api_spec_dir,
            "api_spec_migrations_dir": api_spec_migrations_dir,
            "api_specs_json": api_specs_json,
            "request_response_dir": request_response_dir,
            "decorator_options_file": decorator_options_file,
            "security_definitions_file": security_definitions_file,
            "serializers_base_dir": serializers_base_dir,
            "definitions_serializers_base_dir": definitions_serializers_base_dir,
            "global_parameters_dir": global_parameters_dir,
            "global_response_dir": global_response_dir,
            "url_file": url_file,
            "view_environments_dir": view_environments_dir,
            "sample_json_dir": sample_json_dir,
            "settings_file": settings_file,
            "mock_views_dir": mock_views_dir,
            "views_dir": views_dir,
            "api_environment_file": api_environment_file,
            "android_base_dir": android_base_dir,
            "api_doc_dir": api_doc_dir,
            "tests_dir": tests_dir,
            "global_jars_dir": global_jars_dir,
            "zappa_settings": zappa_settings,
            "apidoc": apidoc,
            "static": static,
            "static_docs": static_docs,
            "docs": docs,
            "interface_dir": interface_dir,
            "mobx_base_dir": mobx_base_dir,
            'mobx_base_dir_models': mobx_base_dir_models,
            'mobx_base_dir_responses': mobx_base_dir_responses,
            'mobx_base_dir_endpoints': mobx_base_dir_endpoints,
            'mobx_base_dir_parameters': mobx_base_dir_parameters,
            "package_json": package_json
        }

    def create_package_json(self):
        """
        creates package_json.json file
        :return:
        """
        f = open(self.paths["package_json"], "w")
        from django_swagger_utils.spec_client.get_package_json import package_json
        f.write(package_json)
        f.close()

    def delete_package_json(self):
        """
        deletes package_json file
        :return:
        """
        os.remove(self.paths["package_json"])

    def install_for_spec(self):
        """
        necessary packages for splitting and merging , 3rd package will be called only if splitting is taking place,
        hence will be installed only during splitting process
        :return:
        """
        self.create_package_json()
        os.system('npm install json-refs')
        os.system('npm install json2yaml')
        os.system('npm install yamljs')
        os.system('npm install swagger-split')  # package only required while splitting hence being installed here
        self.delete_package_json()

    def merge_spec(self):
        """
        Merges the spec file if the api_spec folder cotains the spec folder which further contains the spec file as small parts
        divided into directories
        :return:
        """
        from django_swagger_utils.spec_client.merge_spec import MergeSpec
        merge_spec = MergeSpec(self.paths['api_spec_dir'], self.paths['base_dir'])
        merge_spec.merge()

    def split_spec(self):
        """
        splits the present api_spec.json into further spec folder divided into smaller bits
        :return:
        """
        from django_swagger_utils.spec_client.split_spec import SplitSpec
        from django_swagger_utils.core.utils.check_path_exists import check_path_exists

        if check_path_exists(os.path.join(self.paths['api_spec_dir'], "specs")):
            from shutil import rmtree
            rmtree(os.path.join(self.paths['api_spec_dir'], "specs"))
        split_spec = SplitSpec(self.paths['api_spec_dir'], self.paths['base_dir'])
        split_spec.split()

    def create_mobx_from_templates(self):
        '''
        This method will create a MobxTemplateGenerator object , which will be helpful to generate
        definitions , responses and endpoints.
        :return:
        '''

        from django_swagger_utils.mobx_client.mobx_client import MobxTemplateGenerator
        mobxtemplategenerator = MobxTemplateGenerator(self.parser, self.app_name, self.paths['mobx_base_dir'])
        mobxtemplategenerator.generate_definitions(self.paths['mobx_base_dir_models'])
        mobxtemplategenerator.generate_responses(self.paths['mobx_base_dir_responses'])
        mobxtemplategenerator.generate_endpoints(self.paths['mobx_base_dir_endpoints'])
        mobxtemplategenerator.generate_parameters(self.paths['mobx_base_dir_parameters'])

    def add_to_npm(self):
        '''
        Credentials to jfrog are needed to upload the mobx classes as npm package. credentials need to be uploaded
        in ~/.npmrc file.
        :return:
        '''
        self.generate_apidoc_patches()
        vnum = self.get_version()

        from django_swagger_utils.mobx_client.mobx_npm_deployment import MobxNpmDeployment
        mobnpmdeployment = MobxNpmDeployment(self.app_name, self.paths, vnum)
        mobnpmdeployment.delete_previous()
        mobnpmdeployment.create_template()
        mobnpmdeployment.compress_to_npm()
        mobnpmdeployment.delete_previous()

    def check_create_settings_file(self):
        """
        checks if settings file is present else writes app name to settings file
        :return:
        """
        path = self.paths["settings_file"]
        from django_swagger_utils.core.utils.check_path_exists import check_path_exists
        settings_file = check_path_exists(path)
        if not settings_file:
            settings_file_contents = "# '%s' settings" % self.app_name
            from django_swagger_utils.core.utils.write_to_file import write_to_file
            write_to_file(settings_file_contents, path)

    def check_build_exists(self):
        """
        checks if build folder exists
        :return:
        """
        path = self.base_dir + "/" + self.app_name + "/" + "build"
        from django_swagger_utils.core.utils.check_path_exists import check_path_exists
        build_dir = check_path_exists(path)
        if build_dir:
            raise Exception("Build Directory Already Exist, please run update_specs_build")

    def generate_interfaces(self):
        '''
        class for Interface Generation and also to generate sample request and response.
        :return:
        '''
        from django_swagger_utils.interface_client.interface_generator import InterfaceGenerator
        interface_generator = InterfaceGenerator(self.app_name, self.parser, self.paths['interface_dir'])
        interface_generator.generate_interfaces()
        # interfacegenerator.generate_sample_request_response()

    def load_spec_file(self, spec_file):
        """
            forms a dict from json and raises exception if not present
        :param spec_file:
        :return:
        """
        from django_swagger_utils.core.utils.check_path_exists import check_path_exists
        spec_file_path = check_path_exists(spec_file)
        # print spec_file_path, spec_file,  self.app_name
        if not spec_file_path:
            raise Exception(" %s/api_specs/api_spec.json missing" % self.app_name)
        with open(spec_file) as f:
            json_text = f.read()
            try:
                self.spec_json = json.loads(json_text)
            except ValueError:
                print "The \"%s/api_specs/api_spec.json\" is not a proper JSON." % self.app_name
                exit(1)

    def validate_swagger(self):
        from swagger_spec_validator.util import get_validator
        validator = get_validator(self.spec_json)
        validator.validate_spec(self.spec_json, spec_url='')

    def custom_spec_validator(self):
        # todo need to check for unsupported features present in the specs_json

        # content-type "application/json", "application/x-www-form-urlencoded", -- multipart/form-data not supported
        # parameter type "formData" not supported
        # custom header parameter name does not match standard http request / response headers
        # path parameters regex must be single group
        # file - parameter types not supported
        # path param value must be single word, no spaces allowed in param name
        # python keywords as key / properties names
        # allOff not supported yet
        # response headers - to _ convertion, naming convertion
        # not allowing 'default' key as response method
        pass

    def parse_swagger_specs(self):
        from django_swagger_utils.core.parsers.swagger_parser import SwaggerParser
        self.parser = SwaggerParser(spec_json=self.spec_json)

    def generate_apidoc_patches(self):
        """
        generates patches for changes in spec
        :return:
        """
        base_path = self.paths["api_doc_dir"]
        from django_swagger_utils.core.utils.mk_dirs import MkDirs
        MkDirs().mk_dir_if_not_exits(file_name=base_path + "/")

        from django_swagger_utils.apidoc_gen.generators.patch_generator import PatchGenerator

        patch_generator = PatchGenerator(self.app_name, self.parser, self.paths, base_path)
        # generating api docs
        patch_generator.generate_json_patch()

    def get_version(self):
        """
        :return: the version of spec file
        """
        import os
        version = 0
        if os.path.exists(self.paths["api_spec_migrations_dir"]):
            version_list = []
            dir_list = os.listdir(self.paths["api_spec_migrations_dir"])
            for dl in dir_list:
                if '_patch.json' in dl:
                    version_num = int(dl.replace("_patch.json", ""))
                    version_list.append(version_num)
            version_list.sort(reverse=False)
            if len(version_list) != 0:
                version = version_list[-1]
        version += 1
        return version

    def generate_patch_build(self, domain):
        # TODO change name of def
        """
        generates docs for patches
        :param domain:
        :return:
        """
        base_path = self.paths["api_doc_dir"]
        self.generate_apidoc_patches()
        from django_swagger_utils.apidoc_gen.generators.patch_generator import PatchGenerator
        patch_generator = PatchGenerator(self.app_name, self.parser, self.paths, base_path)
        patch_generator.filter_for_deleted_apis()

        process = subprocess.Popen(['which', 'apidoc'], stdout=subprocess.PIPE)

        output = process.communicate()[0]
        if output:

            with open(self.paths["base_dir"] + "/apidoc.json", 'w') as outfile:
                apidoc_content = {"url": "https://ib-backend-dev.apigateway.in",
                                  "version": "0.0.1",
                                  "description": "",
                                  "name": "iBHubs_backend API Documentation",
                                  "title": "iBHubs_backend Documenation"}
                json.dump(apidoc_content, outfile, indent=4)
            # by default we assume user is working at no specific branch so we fix
            # url to default above url as above , then we check if any specific parametr is given
            # and replace url with required url
            if domain != '' and domain:
                with open(self.paths["apidoc"]) as src_json:
                    apidoc_content = json.load(src_json)
                    apidoc_content['url'] = "https://" + domain
                with open(self.paths["apidoc"], 'w') as outfile:
                    json.dump(apidoc_content, outfile, indent=4)
            try:
                os.mkdir("docs")
            except OSError:
                pass
            # the below command is responsible for creating docs
            process = subprocess.Popen(['apidoc', '-i', self.base_dir,
                                        '-o', os.path.join(self.base_dir, 'docs'),
                                        '-e', 'django_swagger_utils/*',
                                        '-e', 'static/*',
                                        ], stdout=subprocess.PIPE)
            print process.communicate()[0]
            ################################################
            # hosting apidoc
            ################################################
            # obtaining the path of static folder of django-swagger-utils
            # django_swagger_utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            # static_folder_path = os.path.join(django_swagger_utils_path, "static")
            # import shutil
            # # create a folder apidoc , delete if previously exists
            # if os.path.exists(os.path.join(static_folder_path, "apidoc")):
            #     shutil.rmtree(os.path.join(static_folder_path, "apidoc"))
            # apidoc_path = os.path.join(static_folder_path, "apidoc")
            #
            # os.mkdir(apidoc_path)

            # from distutils.dir_util import copy_tree
            # copydocs from docs to apidoc in swagger utils
            # try:
            #     copy_tree(os.path.join(self.base_dir, 'docs'), apidoc_path)
            # except Exception as err:
            #     print err

            # browse to localhost:<port>/static/apidoc/index.html

        else:
            raise CommandError("Help: Install apidoc: [ sudo npm install -g apidoc ]")

    def generate_specs_build(self):
        """
        generates the elements present in spec file
        :return:
        """
        from django_swagger_utils.drf_server.generators.swagger_generator import SwaggerGenerator

        swagger_gen = SwaggerGenerator(self.parser, self.paths, self.app_name)
        # generating request_response files
        swagger_gen.generate_request_response()
        # testing properties
        swagger_gen.generate_definitions()
        # generating global parameters
        swagger_gen.generate_parameters()
        # generating global response
        swagger_gen.generate_responses()
        # generating urls
        swagger_gen.generate_urls()

    def android_build(self):
        """
        generate and deploys jar file
        firstfind thelates evrsion number following which generate jar and deploy it
        :return:
        """

        self.generate_apidoc_patches()
        vnum = self.get_version()
        self.android_jar_genaration(vnum)
        self.android_jar_deployment(vnum)

    def android_jar_genaration(self, vnum):
        """
        generates jar
        :param vnum: version number
        :return:
        """
        base_path = self.paths["android_base_dir"]
        from django_swagger_utils.android_client.generators.android_generator import AndroidGenerator
        android_gen = AndroidGenerator(self.app_name, self.parser, self.paths, base_path)

        # generating all android models
        android_gen.generate_all_models()

        # generating android requests
        android_gen.generate_android_requests_responses()

        # generating android server_gen commands
        android_gen.generate_android_server_commands()

        # generating jar files
        android_gen.generate_jars(vnum)

    def android_jar_deployment(self, vnum):
        """
        deploys the jar in the remote artifactory
        :param vnum: version number
        :return:
        """
        from django_swagger_utils.android_client.generators.android_deployment import AndroidJarDeployment
        base_path = self.paths["android_base_dir"]
        android_deploy = AndroidJarDeployment(self.app_name, self.parser, self.paths, base_path)
        android_deploy.jar_deployment(vnum)

    def android_build_v2(self):
        """
       generate and deploys jar file for version 2
       firstfind thelates evrsion number following which generate jar and deploy it
       :return:
       """
        self.generate_apidoc_patches()
        vnum = self.get_version()
        self.android_jar_v2_genaration(vnum)
        self.android_jar_v2_deployment(vnum)

    def android_jar_v2_genaration(self, vnum):
        """
        generates the jar for the spec
        :param vnum: version number
        :return:
        """
        base_path = self.paths["android_base_dir"]
        from django_swagger_utils.android_client_v2.generators_v2.android_generator_v2 import AndroidGeneratorV2
        android_gen = AndroidGeneratorV2(self.app_name, self.parser, self.paths, base_path)

        # generating all android models
        android_gen.generate_all_models_v2()

        # generating android requests
        android_gen.generate_android_requests_responses_v2()

        # generating android server_gen commands
        android_gen.generate_android_server_commands_v2()

        # generating jar files
        android_gen.generate_jars_v2(vnum)

    def android_jar_v2_deployment(self, vnum):
        """
        deploys the jar in remote artifactory
        :param vnum: version number
        :return:
        """
        base_path = self.paths["android_base_dir"]
        from django_swagger_utils.android_client_v2.generators_v2.android_deployment_v2 import AndroidJarDeploymentV2
        android_deploy = AndroidJarDeploymentV2(self.app_name, self.parser, self.paths, base_path)
        android_deploy.jar_deployment_v2(vnum)

    def build_all(self):
        """
        builds apis jar docs and interfaces
        :return:
        """
        self.android_build()
        self.generate_patch_build('')
        self.generate_specs_build()
        self.generate_interfaces()

    def clean(self):
        """
        deletes the build and docs
        :return:
        """
        if os.path.exists(self.paths['build_dir']):
            shutil.rmtree(self.paths['build_dir'])
        if os.path.exists(os.path.join(self.base_dir, 'docs')):
            shutil.rmtree(os.path.join(self.base_dir, 'docs'))

    @property
    def swagger_generator(self):
        from django_swagger_utils.drf_server.generators.swagger_generator import SwaggerGenerator
        swagger_gen = SwaggerGenerator(self.parser, self.paths, self.app_name)
        return swagger_gen


class Command(BaseCommand):
    can_import_settings = True
    help = 'Generate views and docs from swagger spec files'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--apis', action='store_true', help='Build API Views')
        parser.add_argument('-t', '--thirdparty', action='store_true', help='Build Third Party API Views')
        parser.add_argument('-l', '--lib', action='store_true',
                            help='Build Third Party API Views in lib directory for google ape')
        parser.add_argument('-d', '--docs', action='store_true', help='Build Docs')
        parser.add_argument('-j', '--jars', action='store_true', help='Build Android Jars')
        parser.add_argument('-j2', '--jarsv2', action='store_true', help='Build Android Jars V2')
        parser.add_argument('-m', '--mobx3', action='store_true', help='To generate mobx classes from templates')
        parser.add_argument('-n', '--npm', action='store_true', help='To upload generated mobx classes to npm library')
        parser.add_argument('-j1_gen', '--jars_v1_generation', action='store_true',
                            help='Build Android Jars Genaration')
        parser.add_argument('-j1_deploy', '--jars_v1_deployment', action='store_true',
                            help='Build Android Jars Deployment')
        parser.add_argument('-j2_gen', '--jars_v2_generation', action='store_true',
                            help='Build Android Jars Genaration')
        parser.add_argument('-j2_deploy', '--jars_v2_deployment', action='store_true',
                            help='Build Android Jars Deployment')
        parser.add_argument('-c', '--clean', action='store_true', help='Clean Builds')
        parser.add_argument('-I', '--install', action='store_true',
                            help='install requirements for merge file splitting and merging')
        parser.add_argument('-M', '--merge', action='store_true',
                            help='Merge the spec file structure present in spec folder in api_spec folder')
        parser.add_argument('-S', '--split', action='store_true',
                            help='Split the present api_spec.json into further folders')
        parser.add_argument('app', nargs='*', type=str)
        parser.add_argument('-i', '--interfaces', action='store_true', help='generate interfaces from spec files')
        parser.add_argument('-b', nargs=1, type=str)

    def handle(self, *args, **options):
        '''
        Handles the concerned activity
        :param args: aruguments user give in command line
        :param options: options to arguments given
        :return:
        '''
        from django.conf import settings
        base_dir = settings.BASE_DIR
        # obtain path of zappa_settings
        zappa_settings = os.path.join(base_dir, "zappa_settings.json")
        # set default domain as empty string
        domain = ''
        django_swagger_utils_settings = settings.SWAGGER_UTILS
        swagger_apps = django_swagger_utils_settings['APPS'].keys()

        third_party_swagger_apps = getattr(settings, 'THIRD_PARTY_SWAGGER_APPS', [])
        # if domain specific url is required
        if options['b']:
            # check for existence of zappas_settings.json
            if os.path.exists(zappa_settings):
                with open(zappa_settings) as src_json:
                    zappa_settings_dict = json.load(src_json)
                    # checking if given branch exists
                    if options['b'][0] in zappa_settings_dict:
                        # replacing defaul domain with branch  domain
                        req_branch = options['b'][0]
                        domain = zappa_settings_dict[req_branch]['domain']
                    else:

                        # terminating
                        print "Given branch %s is not found" % options['b'][0]
                        exit(1)
            else:
                print "zappa_settings.json not found"
                exit(1)

        try:
            apps = options['app']
            if not apps:
                apps = swagger_apps

            # calling the concerned build methods for each app
            for app in apps:
                if app in swagger_apps:
                    build = Build(app, base_dir, django_swagger_utils_settings)
                    if options['apis']:
                        build.clean()
                        build.generate_specs_build()

                    if options['docs']:
                        build.generate_patch_build(domain)
                    if options['jars']:
                        Build(app, base_dir, django_swagger_utils_settings).android_build()
                    if options['jarsv2']:
                        Build(app, base_dir, django_swagger_utils_settings).android_build_v2()

                    if options['jars_v1_generation']:
                        vnum = build.get_version()
                        build.android_jar_genaration(vnum)
                    if options['jars_v1_deployment']:
                        vnum = build.get_version()
                        build.android_jar_deployment(vnum)
                    if options['jars_v2_generation']:
                        vnum = build.get_version()
                        build.android_jar_v2_genaration(vnum)
                    if options['jars_v2_deployment']:
                        vnum = build.get_version()
                        build.android_jar_v2_deployment(vnum)
                    if options['clean']:
                        build.clean()
                    if options['interfaces']:
                        build.generate_interfaces()
                    if options['mobx3']:
                        # to generate mobx classes in a folder mobx_classes in build folder
                        build.create_mobx_from_templates()
                    if options['npm']:
                        # to deploy the generated mobx classes under the name ib_appname_mobx
                        build.add_to_npm()

                    if options['install']:
                        # ->install necessary packages for merging and splitting the spec file
                        build.install_for_spec()
                    if options['merge']:
                        # ->merge the spec file which is present in parts in api_spec/specs folder
                        build.merge_spec()
                    if options['split']:
                        # ->split the spec file api_spec.json to specs/ folder
                        build.split_spec()



                else:
                    print ("Ignoring %s app. Please add it in SWAGGER_UTILS['APPS'] first.")

            if options['thirdparty']:
                if options["lib"]:
                    third_party_base_dir = base_dir + "/lib"
                else:
                    third_party_base_dir = os.environ.get('VIRTUAL_ENV')
                    if not third_party_base_dir:
                        print("please run inside a virtual env")
                    third_party_base_dir += "/lib/python2.7/site-packages/"
                for third_party_app in third_party_swagger_apps:
                    build = Build(app_name=third_party_app, base_dir=third_party_base_dir)
                    build.clean()
                    build.generate_specs_build()
        except Exception, err:
            print err
            raise


"""
Open API Specs (swagger.io) - DRF Server - IB Group

1. git clone https://bitbucket.org/rahulsccl/ib_service/
2. pip install -r requirements.txt
3. Open API Specs defined for app_b in app_b/api_specs/api_spec.json Ref
[Open API Specs](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md)
4. python common/swagger/utils/management/build_common.py [ this will generate spces base api server_gen ]
5. manage.py test <app_name>.build.tests
6. python manage.py runserver
7. look at 127.0.0.1:8000/api/app_b/user/1234/
"""

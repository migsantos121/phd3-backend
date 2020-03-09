import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    can_import_settings = True
    help = 'Generate views and docs from swagger spec files'

    def add_arguments(self, parser):
        parser.add_argument('-j', '--jars', action='store_true', help='Push JARs to S3.')
        parser.add_argument('-d', '--docs', action='store_true', help='Push Docs to S3.')
        parser.add_argument('-l', '--local', action='store_true', help='Push Docs to S3.')
        parser.add_argument('--bucket', action='store', help='Name of the S3 bucket to push to.', required=True)
        parser.add_argument('--region', action='store', help='Region to upload.',
                            default='eu-west-1')
        parser.add_argument('--prefix', action='store', help='S3 path prefix to upload to.', default='')
        parser.add_argument('--source', action='store', help='Local path prefix to upload to.', default='')

    def handle(self, *args, **options):
        if options['docs']:
            self.upload_dir_files('docs', options)
        if options['jars']:
            self.upload_dir_files('android_jars', options)
        if options['local']:
            self.upload_dir_files(options['source'], options)

    def upload_dir_files(self, dir_name, options):
        import boto3
        from django.conf import settings
        base_dir = settings.BASE_DIR
        try:
            dir_path = os.path.join(base_dir, dir_name)
            if os.path.exists(dir_path):
                s3 = boto3.client('s3', region_name=options['region'], config= boto3.session.Config(signature_version='s3v4'))
                for base_dir, folders, files in os.walk(dir_path):
                    for file_name in files:
                        file_path = os.path.join(base_dir, file_name)
                        key = os.path.join(options['prefix'], os.path.relpath(file_path, dir_path))
                        content_type = 'text/plain'
                        if '.' in file_name:
                            extension = file_name.split('.')[-1]
                            if extension == 'js':
                                content_type = 'application/x-javascript'
                            elif extension in ['css', 'html']:
                                content_type = 'text/' + extension
                        s3.upload_file(file_path, options['bucket'], key, ExtraArgs={'ContentType': content_type})
            else:
                self.stderr.write("%s Not found" % dir_path)
        except Exception, err:
            print err
            exit(1)
            raise

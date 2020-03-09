import os


from phd3_backend.settings.base import *
from phd3_backend.settings.gae_mysql import *
from phd3_backend.settings.base_swagger_utils import *
from phd3_backend.settings.base_aws_s3 import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

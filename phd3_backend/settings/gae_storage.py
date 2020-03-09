import os

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

GS_ACCESS_KEY_ID = os.environ['GS_ACCESS_KEY_ID']
GS_SECRET_ACCESS_KEY = os.environ['GS_SECRET_ACCESS_KEY']
GS_BUCKET_NAME = os.environ['GS_BUCKET_NAME']

DEFAULT_FILE_STORAGE = 'storages.backends.gs.GSBotoStorage'
STATICFILES_STORAGE = 'storages.backends.gs.GSBotoStorage'

MEDIA_URL = '/media/'
STATIC_URL = '/static/'


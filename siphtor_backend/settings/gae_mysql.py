import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ['MYSQL_HOST'],
        'NAME': os.environ['MYSQL_NAME'],
        'USER': os.environ['MYSQL_USER'],
        'PORT': os.environ.get('MYSQL_POST', 3306),
        'PASSWORD': os.environ['MYSQL_PASSWORD'],
        # 'OPTIONS': {'charset': 'utf8mb4'},
        'OPTIONS': {
             "init_command": "SET foreign_key_checks = 0;",
        }
    }
}

from .base import *
import json
from django.core.exceptions import ImproperlyConfigured

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as json_file:
    secrets = json.load(json_file)


SECRET_KEY = secrets["SECRET_KEY"]
DB_NAME = secrets["DB_NAME"]
DB_USER = secrets["DB_USER"]
DB_PASSWORD = secrets["DB_PASSWORD"]
DB_HOST = secrets["DB_HOST"]

# def get_secret(setting, secrets=secrets):
#     try:
#
#         return secrets[setting]
#     except KeyError:
#         error_msg = "Set the {0} enviroment variable".format(setting)
#         raise ImproperlyConfigured(error_msg)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME, # DB명
        'USER': DB_USER, # 데이터베이스 계정
        'PASSWORD': DB_PASSWORD, # 계정 비밀번호
        'HOST': DB_HOST, # 데이테베이스 주소(IP)
        'PORT': '3306', # 데이터베이스 포트(보통은 3306)
        'OPTIONS': {
            #'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO'",
            'charset': 'utf8mb4'
        },


    }
}

DEBUG = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media',)

# AWS S3

AWS_ACCESS_KEY_ID = secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = secrets["AWS_SECRET_ACCESS_KEY"]
AWS_DEFAULT_ACL = secrets["AWS_DEFAULT_ACL"]
AWS_REGION = secrets["AWS_REGION"]
AWS_STORAGE_BUCKET_NAME = secrets["AWS_STORAGE_BUCKET_NAME"]
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
DEFAULT_FILE_STORAGE = 'jellybank.storages.S3DefaultStorage'
STATICFILES_STORAGE = 'jellybank.storages.S3StaticStorage'

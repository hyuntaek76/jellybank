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
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },


    }
}

DEBUG = False

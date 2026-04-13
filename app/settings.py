# coding: utf-8

import logging

from environs import Env

env = Env()
env.read_env()

# [ VARS ]
MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24


# [ TRACE ]
TEST = env.bool('TEST', default=False)
DEBUG = TEST
LOGLEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=LOGLEVEL, format='%(levelname)s - %(asctime)s - %(message)s')


# [ DATABASE ]
DATABASE_TYPE = env.str('DATABASE_TYPE', default='sqlite3')
DATABASE_SERVER = env.str('DATABASE_SERVER', default='')
DATABASE_USERNAME = env.str('DATABASE_USER', default='')
DATABASE_PASSWORD = env.str('DATABASE_PASSWORD', default='')
DATABASE_NAME = env.str('DATABASE_NAME', default='')

DATABASES_URL_TEMPLATES = {
    'sqlite3': 'sqlite+aiosqlite:///db.sqlite3',
    'mysql': 'mysql+aiomysql://{username}:{password}@{server}/{database}',
    'postgresql': 'postgresql+asyncpg://{username}:{password}@{server}/{database}',
}

DATABASE_URL = DATABASES_URL_TEMPLATES[DATABASE_TYPE].format(
    database=DATABASE_NAME, server=DATABASE_SERVER,
    username=DATABASE_USERNAME, password=DATABASE_PASSWORD,
)


# [OAUTH UI]
OAUTH_UI_URI = env.str('OAUTH_UI_URI', default='http://localhost:5173')
OAUTH_UI_LOGIN_URL = f'{OAUTH_UI_URI}/login'
OAUTH_UI_CONSENT_URL = f'{OAUTH_UI_URI}/consent'
OAUTH_USER_ACCOUNT_URL = f'{OAUTH_UI_URI}/account'


# [COOKIES]
UI_COOKIES_EXPIRE_NAME = 'UI_COOKIES'
UI_COOKIES_EXPIRE_SECONDS = env.int('UI_COOKIES_EXPIRE_SECONDS', default=3*HOUR)
UI_COOKIES_ONLY_ON_HTTPS = False


# [JWT]
JWT_SECRET_KEY = env.str('JWT_SECRET_KEY', default='1234')
JWT_ALGORITHM = env.str('JWT_ALGORITHM', default='HS256')


# [OTP]
OTP_MAX_ATTEMPTS = env.int('OTP_MAX_ATTEMPTS', default=5)
OTP_EXPIRE_SECOND = env.int('OTP_EXPIRE_SECOND', default=3*MINUTE)


# [OAUTH BACKEND]
OAUTH_API_PREFIX = env.str('OAUTH_API_PREFIX', default='/oauth2')
OAUTH_API_URI = env.str('OAUTH_API_URI', default='localhost:8000')

# []
REQUEST_AUTHORIZATION_EXPIRE_SECONDS = env.int('REQUEST_AUTHORIZATION_EXPIRE_SECONDS', default=3*MINUTE)
AUTHORIZATION_CODE_EXPIRE_SECONDS = env.int('AUTHORIZATION_CODE_EXPIRE_SECONDS', default=MINUTE)

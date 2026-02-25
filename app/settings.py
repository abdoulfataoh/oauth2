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
    'sqlite3': {
        'url': 'sqlite+aiosqlite:///db.sqlite3',
    },

    'mysql': {
        'url': 'mysql://{username}:{password}@{server}/{database}'
    },

    'postgresql': {
        'url': 'postgresql://{username}:{password}@{server}/{database}'
    }
}

DATABASE_URL = DATABASES_URL_TEMPLATES[DATABASE_TYPE]['url'].format(
    database=DATABASE_NAME, server=DATABASE_SERVER,
    username=DATABASE_USERNAME, password=DATABASE_PASSWORD,
)


# [JWT]
JWT_SECRET_KEY = env.str('JWT_SECRET_KEY', default='1234')
JWT_ALGORITHM = env.str('JWT_ALGORITHM', default='HS256')


# [OAUTH BACKEND]
OAUTH_API_PREFIX = env.str('OAUTH_API_PREFIX', default='/oauth2')
OAUTH_API_URI = env.str('OAUTH_API_URI', default='localhost:8000')

# [TOKEN & EXPIRE TIME]
UI_ACCESS_TOKEN_EXPIRE_MINUTES = env.int('ACCESS_TOKEN_EXPIRE_MINUTES', default=3*HOUR)
AUTHORIZATION_CODE_EXPIRE_MINUTES = env.int('AUTHORIZATION_CODE_EXPIRE_MINUTES', default=5*DAY)
REQUEST_AUTHORIZATION_EXPIRE_TIME = env.int('REQUEST_EXPIRE_TIME', default=3*MINUTE)

# [OAUTH UI]
OAUTH_UI_URI = env.str('OAUTH_UI_URI', default='http://localhost:5173')
OAUTH_UI_LOGIN_URL = f'{OAUTH_UI_URI}/login'
OAUTH_UI_CONSENT_URL = f'{OAUTH_UI_URI}/consent'

# coding: utf-8

import logging

from environs import Env


env = Env()
env.read_env()

# [ Trace ]
TEST = env.bool('TEST', default=True)
DEBUG = TEST

if TEST:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL, format='%(levelname)s - %(asctime)s - %(message)s')

# [ Database ]
DATABASES = {
    'default': {
        'url': 'sqlite+aiosqlite:///db.sqlite3',
    },

    'mysql': {
        'url': 'mysql://{user}:{password}@{server}/{db}'
    },

    'postgresql': {
        'url': 'postgresql://{user}:{password}@{server}/{db}'
    }
}

DATABASE_USER = env.str('DATABASE_USER', default='')
DATABASE_PASSWORD = env.str('DATABASE_PASSWORD', default='')
DATABASE_SERVER = env.str('DATABASE_SERVER', default='')
DATABASE_NAME = env.str('DATABASE_NAME', default='vela')

DB = 'default' if TEST else 'mysql'

SQLALCHEMY_DATABASE_URL = DATABASES[DB]['url'].format(
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    server=DATABASE_SERVER,
    db=DATABASE_NAME
)

# [ Authentification Server ]
AUTH_SERVER_AUTHORIZATION = env.str('AUTH_SERVER_AUTHORIZATION', default='http://localhost:8000/oauth2/authorization')
AUTH_SERVER_TOKEN = env.str('AUTH_SERVER_TOKEN', default='http://localhost:8000/oauth2/token')
OAUTH2_SECRET_KEY = env.str('OAUTH2_SECRET_KEY', default='')
OAUTH2_ALGORITHM = env.str('OAUTH2_ALGORITHM', default='HS256')
OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES = env.int('OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES', default=30)

# [ General ]
TIMEZONE = env.str('TIMEZONE', default='UTC')

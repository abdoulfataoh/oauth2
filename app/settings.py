# coding: utf-8

import logging

from environs import Env


env = Env()
env.read_env()

# Vars
MINUTE = 60
HOUR = MINUTE * 60

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
DATABASE_NAME = env.str('DATABASE_NAME', default='')

DB = 'default' if TEST else 'mysql'

_DATABASE_URL_ = DATABASES[DB]['url'].format(
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    server=DATABASE_SERVER,
    db=DATABASE_NAME
)
DATABASE_URL = env.str('DATABASE_URL', default=_DATABASE_URL_)

# [ Secret ]
SECRET_KEY = env.str('SECRET_KEY', default='1234')
JWT_ALGORITHM = env.str('JWT_ALGORITHM', default='HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = env.int('ACCESS_TOKEN_EXPIRE_MINUTES', default=60*60)

# [ General ]
TIMEZONE = env.str('TIMEZONE', default='UTC')

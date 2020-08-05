

import os


SECRET_KEY = os.urandom(16)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

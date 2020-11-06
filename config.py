from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY')

    """Base config"""

    user = environ.get('POSTGRES_USER')
    password = environ.get('POSTGRES_PASSWORD')
    host = environ.get('POSTGRES_HOST')
    port = environ.get('POSTGRES_PORT')
    database = environ.get('POSTGRES_DB')

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

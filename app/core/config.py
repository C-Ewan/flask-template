from os import getenv
from dotenv import load_dotenv


load_dotenv()

class Config: 
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL') or 'sqlite:///database.db' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    DEBUG = False

    if SECRET_KEY is None:
        from warnings import warn
        from random import choices
        from string import ascii_letters, digits
        SECRET_KEY = ''.join(choices(ascii_letters + digits, k=20))

        warn('SECRET_KEY is not set. A random secret key has been generated '
             'for this environment. Make sure to set the SECRET_KEY in '
             'production to maintain session consistency and security.', UserWarning)

class DevelopmentConfig(Config): 
    DEBUG = True 
    SQLALCHEMY_ECHO = True # To view SQL queries in the console

class TestingConfig(Config): 
    TESTING = True 
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL') or 'sqlite:///database_test.db' 
    SQLALCHEMY_ECHO = False 
    WTF_CSRF_ENABLED = False # Disable CSRF for testing
    
class ProductionConfig(Config):
    pass

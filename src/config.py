from os import getenv
from datetime import timedelta
from dotenv import load_dotenv


load_dotenv()


class ConfigurationError(Exception):
    pass


SECRET_KEY = getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
JWT_ACCESS_TOKEN_EXPIRES = getenv("ACCESS_TOKEN_EXPIRES") or 3600
FLASK_ENV = getenv("FLASK_ENV", "development")

if SECRET_KEY is None:
    raise ConfigurationError("'SECRET_KEY' environment variable is not set.")

if SQLALCHEMY_DATABASE_URI is None:
    raise ConfigurationError("'DATABASE_URL' environment variable is not set.")

if not isinstance(JWT_ACCESS_TOKEN_EXPIRES, int):
    try:
        JWT_ACCESS_TOKEN_EXPIRES = int(JWT_ACCESS_TOKEN_EXPIRES)
    except Exception as e:
        raise ConfigurationError(
            "'ACCESS_TOKEN_EXPIRES' must be a positive integer."
        ) from e

if JWT_ACCESS_TOKEN_EXPIRES <= 0:
    raise ConfigurationError("'ACCESS_TOKEN_EXPIRES' must be greater than 0.")


class Config:
    SECRET_KEY = SECRET_KEY
    DEBUG = __debug__
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # To view SQL queries in the console


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL_TESTING") or "sqlite:///:memory:"
    SQLALCHEMY_ECHO = False
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing


class ProductionConfig(Config):
    DEBUG = False

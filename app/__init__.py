from os import getenv

from flask import Flask

from .core import (
    ProductionConfig,
    TestingConfig,
    DevelopmentConfig,

    APIException,
    handle_api_exception,

    db,
    migrate,
    cors,
    init_extensions
)


def create_app():
    app = Flask(__name__)

    # Select configuration based on environment variable
    match getenv('FLASK_ENV', 'development'):
        case 'production':
            app.config.from_object(ProductionConfig) 
        case 'testing':
            app.config.from_object(TestingConfig) 
        case 'development' | _:
            app.config.from_object(DevelopmentConfig)

    # Init Extensions
    init_extensions(app)

    # Blueprints (Routes, ...)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Register error handlers
    app.register_error_handler(APIException, handle_api_exception)

    return app
    
from flask import Flask
from werkzeug.exceptions import (
    BadRequest,
    Unauthorized,
    Forbidden,
    RequestEntityTooLarge,
    UnsupportedMediaType,
    UnprocessableEntity,
    TooManyRequests,
)
from src.extensions import init_extensions
from src.config import (
    ConfigurationError,
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
    FLASK_ENV,
)
from src.utils.handlers import make_default_handler, ApiError, handler_api_error
from src.routes import v1


def create_app() -> Flask:
    app = Flask(__name__)

    match FLASK_ENV:
        case "production":
            app.config.from_object(ProductionConfig)
        case "testing":
            app.config.from_object(TestingConfig)
        case "development":
            app.config.from_object(DevelopmentConfig)
        case _:
            raise ConfigurationError(
                f"Unsupported FLASK_ENV value: '{FLASK_ENV}'. Use 'production', 'testing', or 'development'."
            )

    app.register_error_handler(ApiError, handler_api_error)
    app.register_error_handler(404, make_default_handler(404))
    app.register_error_handler(405, make_default_handler(405))

    app.register_error_handler(BadRequest, make_default_handler(400))
    app.register_error_handler(Unauthorized, make_default_handler(401))
    app.register_error_handler(Forbidden, make_default_handler(403))
    app.register_error_handler(RequestEntityTooLarge, make_default_handler(413))
    app.register_error_handler(UnsupportedMediaType, make_default_handler(415))
    app.register_error_handler(UnprocessableEntity, make_default_handler(422))
    app.register_error_handler(TooManyRequests, make_default_handler(429))

    init_extensions(app)

    app.register_blueprint(v1)

    app.url_map.strict_slashes = False

    return app

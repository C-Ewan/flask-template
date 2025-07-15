from http import HTTPStatus
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from src.utils.response import Response
from src.utils.misc import to_flask_response


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()


def init_extensions(app: Flask):
    """Initialize all extensions with the Flask application."""
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # JWT
    jwt.init_app(app)

    from src.models.auth import RevokedToken
    from src.models.user import User

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(header: dict[str, str], payload: dict[str, str]) -> bool:
        if (
            (not "jti" in payload)
            or (not "version" in payload)
            or (not "user" in payload)
        ):
            return True

        user_uuid = payload["user"]

        if RevokedToken.exist(jti=payload["jti"], user_uuid=user_uuid):
            return True

        user = User.query.filter_by(uuid=user_uuid).first()
        if not isinstance(user, User):
            return True

        return user.session_version != payload["version"]

    @jwt.token_verification_failed_loader
    def token_verification_failed_loader(header, payload):
        return to_flask_response(
            Response(HTTPStatus.BAD_REQUEST, "User claims verification failed")
        )

    @jwt.user_lookup_error_loader
    def user_lookup_error_loader(h, p):
        return to_flask_response(
            Response(HTTPStatus.UNAUTHORIZED, "Error loading user")
        )

    @jwt.revoked_token_loader
    def revoked_token_loader(h, p):
        return to_flask_response(
            Response(HTTPStatus.UNAUTHORIZED, "Token has been revoked")
        )

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_loader(h, p):
        return to_flask_response(
            Response(HTTPStatus.UNAUTHORIZED, "Fresh token required")
        )

    @jwt.unauthorized_loader
    def unauthorized_loader(error_string: str):
        return to_flask_response(Response(HTTPStatus.UNAUTHORIZED, error_string))

    @jwt.invalid_token_loader
    def invalid_token_loader(error_string: str):
        return to_flask_response(
            Response(HTTPStatus.UNPROCESSABLE_ENTITY, error_string)
        )

    @jwt.expired_token_loader
    def expired_token_loader(h, p):
        return to_flask_response(Response(401, "Token has expired"))

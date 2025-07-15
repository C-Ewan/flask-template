from datetime import datetime, timezone
from http import HTTPStatus
from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from pydantic import BaseModel, Field
from src.extensions import db
from src.models import User, RevokedToken
from src.routes.utils import req_json
from src.utils.handlers import ApiError, handle_api_errors
from src.utils.response import Response
from src.utils.misc import to_flask_response


auth_api = Blueprint("auth_api", __name__)


# Schemas
class SchemaUserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=10, pattern=r"^[a-zA-Z].*")
    password: str = Field(min_length=8, max_length=100)


@auth_api.route("/signup", methods=["POST"])
@handle_api_errors
@req_json(model=SchemaUserLogin, parameter_name="body")
def _signup(body: SchemaUserLogin):
    username = body.username.lower()
    password = body.password

    if User.exist(username=username):
        raise ApiError(HTTPStatus.BAD_REQUEST, "user already exist")

    new_user = User.create(username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return to_flask_response(
        Response(200, data=new_user.to_dict("password_hash", "session_version"))
    )


@auth_api.route("/login", methods=["POST"])
@handle_api_errors
@req_json(model=SchemaUserLogin, parameter_name="body")
def _login(body: SchemaUserLogin):
    username = body.username.lower()
    password = body.password

    user = User.query.filter_by(username=username).first()

    if not isinstance(user, User) or not user.check_password(password):
        raise ApiError(HTTPStatus.UNAUTHORIZED, "invalid credentials")

    return to_flask_response(
        Response(
            HTTPStatus.OK,
            data=user.to_dict("password_hash", "session_version")
            | {
                "token": create_access_token(
                    user.uuid,
                    additional_claims={
                        "version": user.session_version,
                        "user": user.uuid,
                    },
                )
            },
        )
    )


@auth_api.route("/logout", methods=["GET", "DELETE"])
@jwt_required()
@handle_api_errors
def _logout():
    # /logout?remove_all=1
    remove_all = request.args.get("remove_all", 0, type=lambda x: bool(int(x)))
    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if isinstance(user, User):
        if remove_all:
            user.session_version += 1
            for rt in RevokedToken.query.filter_by(user_uuid=user.uuid).all():
                db.session.delete(rt)
        else:
            token_payload = get_jwt()
            jti = token_payload.get("jti", "")
            tokentype = token_payload.get("type", "")
            exp_timestamp = token_payload.get("exp")
            exp_at = (
                datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
                if exp_timestamp
                else datetime.now(timezone.utc)
            )

            db.session.add(RevokedToken.create(user.uuid, jti, tokentype, exp_at))
        db.session.commit()
    return to_flask_response(Response(HTTPStatus.OK, "logout successful"))

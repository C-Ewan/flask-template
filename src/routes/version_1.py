from flask import Blueprint
from src.routes.auth import auth_api


v1 = Blueprint("version_1", __name__, url_prefix="/v1")

v1.register_blueprint(auth_api)

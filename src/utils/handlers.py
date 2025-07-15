from functools import wraps
from http import HTTPStatus
from flask import request
from src.utils.misc import to_flask_response
from src.utils.response import Response as ApiResponse


class ApiError(ApiResponse, Exception):
    def __init__(
        self,
        code: HTTPStatus | int,
        msg: str | None = None,
        errors=None,
        data=None,
        _timestamp: str | None = None,
    ) -> None:
        ApiResponse.__init__(self, code, msg, errors, data, _timestamp)
        Exception.__init__(self, f"HTTPError(code={int(self.code)}, msg={self.msg!r})")


def make_default_handler(status: HTTPStatus | int):
    def handler(error: Exception):
        return to_flask_response(
            ApiResponse(
                status, data={"path": request.full_path, "method": request.method}
            )
        )

    return handler


def handler_api_error(error: ApiError):
    return to_flask_response(error)


def handle_api_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, ApiError):
                raise e
            raise ApiError(500)

    return wrapper

from collections.abc import Callable
from functools import wraps
from http import HTTPStatus
from flask import request
from flask.typing import ResponseReturnValue
from pydantic import BaseModel, ValidationError
from src.utils.handlers import ApiError


def req_json[**P](
    *, model: type[BaseModel] | None = None, parameter_name: str = "body"
):
    def decorator(fn: Callable[P, ResponseReturnValue]):
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs):
            raw = request.get_json(silent=True)
            if raw is None:
                raise ApiError(
                    HTTPStatus.BAD_REQUEST,
                    "Missing JSON payload",
                    [{"field": "", "message": "Expected JSON body."}],
                )
            if model:
                if not isinstance(raw, dict):
                    raise ApiError(
                        HTTPStatus.BAD_REQUEST,
                        "JSON must be an object",
                        [{"field": "", "message": "Received non-dict JSON."}],
                    )
                try:
                    validated = model(**raw)
                except ValidationError as e:
                    details = [
                        {
                            "field": ".".join(str(x) for x in err["loc"]),
                            "message": err["msg"],
                        }
                        for err in e.errors()
                    ]
                    raise ApiError(HTTPStatus.BAD_REQUEST, "Invalid JSON", details)

                kwargs[parameter_name] = validated
            else:
                kwargs[parameter_name] = raw
            return fn(*args, **kwargs)

        return wrapper

    return decorator

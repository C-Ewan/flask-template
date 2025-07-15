from flask import jsonify
from flask.typing import ResponseReturnValue
from src.utils.response import Response as ApiResponse


def omit_keys[K, V](o: dict[K, V], *keys: K) -> dict[K, V]:
    r = o.copy()
    for k in keys:
        if k in r:
            del r[k]
    return r


def to_flask_response(res: ApiResponse) -> ResponseReturnValue:
    c, code = res.to_response()
    return jsonify(c), code

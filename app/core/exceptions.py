from typing import (
    Optional,
    Iterable,
    Any,
    Tuple,
    Dict
)

from flask import (
    jsonify,
    Response
)


class APIException(Exception):
    status_code = 400

    def __init__(self, message: str, status_code: Optional[int] = None, 
                 payload: Optional[Iterable[Tuple[str, Any]]] = None) -> None:
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.payload or ()) | { 'message': self.message }
    
def handle_api_exception(error) -> Response: 
    response = jsonify(error.to_dict()) 
    response.status_code = error.status_code 
    return response
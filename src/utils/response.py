from datetime import datetime, timezone
from http import HTTPStatus


class Response:
    def __init__(
        self,
        code: HTTPStatus | int,
        msg: str | None = None,
        errors=None,
        data=None,
        _timestamp: str | None = None,
    ) -> None:
        self.code = code if isinstance(code, HTTPStatus) else HTTPStatus(code)
        self.data = data if data else None
        self.msg = msg or self.code.phrase
        self.errors = errors
        self.timestamp = (
            datetime.now(timezone.utc)
            if _timestamp is None
            else datetime.fromisoformat(_timestamp)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({int(self.code)!r}, {self.msg!r}, {self.errors!r}, {self.data!r}, {str(self.timestamp)!r})"

    def to_response(self) -> tuple[dict, int]:
        return {
            "msg": self.msg,
            "data": self.data,
            "errors": self.errors,
            "timestamp": self.timestamp,
        }, int(self.code)

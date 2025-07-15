from typing import Any
from functools import cache
from sqlalchemy.orm import InstrumentedAttribute
from src.extensions import db
from src.utils.misc import omit_keys


class Base(db.Model):
    __abstract__ = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    @cache
    def cols(cls):
        return [
            k for k, v in cls.__dict__.items() if isinstance(v, InstrumentedAttribute)
        ]

    def __repr__(self) -> str:
        return f"<{type(self).__name__}() />"

    def to_dict(self, *omit: str) -> dict[str, Any]:
        return omit_keys({x: getattr(self, x) for x in self.cols()}, *omit)

    @classmethod
    def exist(cls, **filter_by: Any) -> bool:
        return bool(
            db.session.query(
                db.session.query(cls).filter_by(**filter_by).exists()
            ).scalar()
        )

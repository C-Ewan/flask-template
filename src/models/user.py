from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import Text, UUID as SQLUUID, DateTime, Integer
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import mapped_column, MappedColumn
from src.models.base import Base


class User(Base):
    __tablename__: str = "users"

    uuid: MappedColumn[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True)
    username: MappedColumn[str] = mapped_column(Text, nullable=False, unique=True)
    visiblename: MappedColumn[str] = mapped_column(Text, nullable=True, unique=False)
    password_hash: MappedColumn[str] = mapped_column(Text, nullable=False)
    session_version: MappedColumn[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    created_at: MappedColumn[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password=password)

    @classmethod
    def create(cls, username: str):
        return cls(
            uuid=uuid4(), username=username, created_at=datetime.now(timezone.utc)
        )

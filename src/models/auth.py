from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, UUID as SQLUUID, DateTime, String
from sqlalchemy.orm import mapped_column, MappedColumn
from src.models.base import Base


class RevokedToken(Base):
    __tablename__ = "revoked_jwt"
    uuid: MappedColumn[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True)
    user_uuid: MappedColumn[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("users.uuid")
    )
    jti: MappedColumn[str] = mapped_column(String(120), unique=True, nullable=False)
    token_type: MappedColumn[str] = mapped_column(String(20), nullable=False)
    revoked_at: MappedColumn[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    expires_at: MappedColumn[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    @classmethod
    def create(cls, user: UUID, jti: str, tokentype: str, expires_at: datetime):
        return cls(
            uuid=uuid4(),
            user_uuid=user,
            jti=jti,
            token_type=tokentype,
            revoked_at=datetime.now(timezone.utc),
            expires_at=expires_at,
        )

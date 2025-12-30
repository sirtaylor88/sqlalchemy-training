"""Second lesson:

- Create a table using Alchemy ORM.
"""

from abc import ABC
from datetime import datetime
from typing import Optional
from sqlalchemy import BIGINT, TIMESTAMP, VARCHAR, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase, ABC):
    """Clone DeclarativeBase for use."""


class User(Base):
    """Telegram user."""

    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
    )
    full_name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    username: Mapped[Optional[str]] = mapped_column(
        VARCHAR(255),
    )
    language_code: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now,
    )
    referrer_id: Mapped[Optional[int]] = mapped_column(
        BIGINT,
        ForeignKey("users.telegram_id", ondelete="SET NULL"),
    )

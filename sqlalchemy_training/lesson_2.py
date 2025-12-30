"""Second lesson:

- Create a table using Alchemy ORM.
- Use mixins to refactor codes.
- Use Annotated to refactor codes.
- Using SQLAlchemy to Create Tables in the Database.
"""

from datetime import datetime
from typing import Annotated, Optional

from sqlalchemy import (
    BIGINT,
    TIMESTAMP,
    VARCHAR,
    ForeignKey,
    Integer,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

int_pk = Annotated[int, mapped_column(Integer, primary_key=True)]
user_pk = Annotated[
    BIGINT,
    mapped_column(
        ForeignKey("users.telegram_id", ondelete="SET NULL"),
        nullable=True,
        autoincrement=False,
    ),
]
str_255 = Annotated[str, mapped_column(VARCHAR(255))]


class TableNameMixin:
    """Mixin to generate table name."""

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Build table name from class name."""

        return cls.__name__.lower() + "s"


class TimestampMixin:
    """Mixin to add timestamps to records."""

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now,
    )


class Base(DeclarativeBase):
    """Clone DeclarativeBase for use."""


class User(TimestampMixin, TableNameMixin, Base):
    """Telegram user."""

    telegram_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
    )
    full_name: Mapped[str_255]
    username: Mapped[Optional[str_255]]
    language_code: Mapped[str_255]
    referrer_id: Mapped[Optional[user_pk]]


class Product(TimestampMixin, TableNameMixin, Base):
    """Product."""

    product_id: Mapped[int_pk]
    title: Mapped[str_255]
    description: Mapped[Optional[str_255]]


class Order(TimestampMixin, TableNameMixin, Base):
    """Order"""

    order_id: Mapped[int_pk]
    user_id: Mapped[user_pk]


class OrderProduct(TableNameMixin, Base):
    """Intermediary table to link orders and products."""

    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        primary_key=True,
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.product_id", ondelete="RESTRICT"),
        primary_key=True,
    )
    quantity: Mapped[int]

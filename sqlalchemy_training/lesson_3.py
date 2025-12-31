"""Third:

- Insert queries using ORM.
- Advanced Select queries.
- Combining Insert, Select and Update in a Single Query
- Seed initial data to the DB.
- ORM Joins queries
"""

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, aliased

from sqlalchemy_training.lesson_1 import session_maker
from sqlalchemy_training.lesson_2 import Order, OrderProduct, Product, User


class Repo:
    """Collection of methods to work on the DB."""

    def __init__(self, sess: Session) -> None:
        self.session = sess

    def add_user(
        self,
        /,
        *,
        telegram_id: int,
        full_name: str,
        lang: str,
        username: Optional[str] = None,
        referrer_id: Optional[int] = None,
    ) -> User:
        """Add new user to DB."""

        stmt = select(User).from_statement(
            insert(User)
            .values(
                telegram_id=telegram_id,
                full_name=full_name,
                language_code=lang,
                user_name=username,
                referrer_id=referrer_id,
            )
            .on_conflict_do_update(
                index_elements=[User.telegram_id],
                set_={
                    "user_name": username,
                    "full_name": full_name,
                },
            )
            .returning(User)
        )

        result = self.session.scalars(stmt)
        self.session.commit()

        return result.first()

    def get_user_by_id(self, telegram_id: int) -> User:
        """Select an user by its ID."""

        stmt = select(User).where(User.telegram_id == telegram_id)
        result = self.session.execute(stmt)
        self.session.commit()

        return result.scalars().first()

    def get_last_ten_users(self) -> Sequence[User]:
        """Select all users in DB."""

        stmt = (
            select(
                User,
            )
            .order_by(
                User.created_at.desc(),
            )
            .limit(10)
        )
        results = self.session.execute(stmt)
        self.session.commit()

        return results.scalars().all()

    def get_user_lang(self, telegram_id: int) -> str:
        """Select an user by its ID."""

        stmt = select(
            User.language_code,
        ).where(
            User.telegram_id == telegram_id,
        )
        result = self.session.execute(stmt)
        self.session.commit()

        return result.scalars()

    def add_order(self, user_id: int) -> Order:
        """Add a new order to the DB."""

        stmt = insert(Order).values(user_id=user_id).returning(Order)

        results = self.session.scalars(stmt)
        self.session.commit()

        return results.first()

    def add_product(
        self,
        title: str,
        price: int,
        description: Optional[str] = None,
    ) -> Product:
        """Add a new product to the DB."""
        stmt = select(Product).from_statement(
            insert(Product)
            .values(title=title, description=description, price=price)
            .returning(Product)
        )

        results = self.session.scalars(stmt)
        self.session.commit()

        return results.first()

    def add_product_to_order(
        self,
        product_id: int,
        order_id: int,
        quantity: int,
    ) -> None:
        """Add a new product to the DB."""
        stmt = (
            insert(OrderProduct)
            .values(
                product_id=product_id,
                order_id=order_id,
                quantity=quantity,
            )
            .on_conflict_do_nothing()
        )

        self.session.execute(stmt)
        self.session.commit()

    def select_all_invited_users(self):
        """Get all invited users."""

        ParentUser = aliased(User)
        ReferralUser = aliased(User)

        stmt = select(
            ParentUser.full_name.label("parent_name"),
            ReferralUser.full_name.label("referrer_name"),
        ).join(ReferralUser, ReferralUser.referrer_id == ParentUser.telegram_id)

        results = self.session.execute(stmt)
        self.session.commit()
        return results.all()


if __name__ == "__main__":
    with session_maker() as session:
        repo = Repo(session)
        for row in repo.select_all_invited_users():
            print(f"Parent: {row.parent_name}, Referral: {row.referrer_name}")

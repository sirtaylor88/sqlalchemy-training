"""Third:

- Insert queries using ORM.
- Advanced Select queries.
- Combining Insert, Select and Update in a Single Query
- Seed initial data to the DB.
- ORM Joins queries.
- Advanced select queries with join.
- Aggregated Queries.
"""

from typing import Optional, Sequence

from sqlalchemy import create_engine, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session, aliased, sessionmaker

from sqlalchemy_training.lesson_1 import database_url
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

    def get_all_users(self) -> Sequence[User]:
        """Select all users in DB."""

        stmt = select(
            User,
        ).order_by(
            User.created_at.desc(),
        )
        results = self.session.execute(stmt)
        self.session.commit()

        return results.scalars().all()

    def get_last_ten_users(self) -> Sequence[User]:
        """Select last ten users in DB."""

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

    def select_all_invited_users(self) -> Sequence[Row[tuple[str, str]]]:
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

    def get_all_user_orders(
        self, telegram_id: int
    ) -> Sequence[Row[tuple[Order, User]]]:
        """Get all orders from an user."""

        stmt = (
            select(
                Product,
                Order,
                User.user_name,
                OrderProduct.quantity,
            )
            .join(OrderProduct)
            .join(Order)
            .join(User)
            .select_from(Product)
            .where(
                User.telegram_id == telegram_id,
            )
        )
        results = self.session.execute(stmt)
        self.session.commit()
        return results.all()

    def get_total_of_orders(self, telegram_id: int) -> int:
        """Get total number of orders from an user."""
        stmt = select(func.count(Order)).where(Order.user_id == telegram_id)
        result = self.session.scalar(stmt)
        self.session.commit()
        return result

    def get_total_of_orders_per_user(self) -> Sequence[Row[tuple[int, str]]]:
        """Get total number of orders per user."""
        stmt = (
            select(func.count(Order), User.full_name)
            .join(User)
            .group_by(User.telegram_id)
        )
        result = self.session.execute(stmt)
        self.session.commit()
        return result.all()

    def get_total_of_ordered_products_per_user(
        self,
    ) -> Sequence[Row[tuple[int, str]]]:
        """Get total number of ordered  productsper user."""
        stmt = (
            select(
                func.sum(OrderProduct.quantity).label("quantity"),
                User.full_name,
            )
            .join(Order, Order.order_id == OrderProduct.order_id)
            .join(User)
            .group_by(User.telegram_id)
        )
        result = self.session.execute(stmt)
        self.session.commit()
        return result.all()


if __name__ == "__main__":
    engine = create_engine(database_url)
    session_maker = sessionmaker(engine)
    with session_maker() as session:
        repo = Repo(session)
        # for row in repo.select_all_invited_users():
        #     print(f"Parent: {row.parent_name}, Referral: {row.referrer_name}")

        # for user in repo.get_all_users():
        #     print(f"User: {user.full_name} ({user.telegram_id})")

        #     for order in user.orders:
        #         print(f"    Order: {order.order_id}")

        #         for product in order.products:
        #             print(f"    - Product: {product.product.title}")

        user_orders = repo.get_all_user_orders(telegram_id=18)
        # for row in user_orders:
        #     print(
        #         f"Product: {row.Product.title}: Order: {row.Order.order_id}: {row.user_name}"
        #     )

        for product, order, user_name, amount in user_orders:
            print(
                f"Product: {product.title} x {amount}: Order: {order.order_id}: {user_name}"
            )

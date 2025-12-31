"""Seed fake data."""

import random

from faker import Faker

from sqlalchemy_training.lesson_1 import session_maker
from sqlalchemy_training.lesson_2 import Order, Product, User
from sqlalchemy_training.lesson_3 import Repo

Faker.seed(0)
fake = Faker()

session = session_maker()
repo = Repo(session)


def delete_records() -> None:
    """Delete all records."""
    session.query(User).delete()
    session.query(Order).delete()
    session.query(Product).delete()
    session.commit()


def seed_fake_data() -> None:
    """Seed fake data."""

    users = []
    orders = []
    products = []

    for _ in range(10):
        referrer_id = None if not users else users[-1].telegram_id
        new_user = repo.add_user(
            telegram_id=fake.pyint(),
            full_name=fake.name(),
            lang=fake.language_code(),
            username=fake.user_name(),
            referrer_id=referrer_id,
        )
        users.append(new_user)

    for _ in range(10):
        new_order = repo.add_order(
            user_id=random.choice(users).telegram_id,
        )
        orders.append(new_order)

    for _ in range(10):
        new_product = repo.add_product(
            title=fake.word(),
            description=fake.sentence(),
            price=fake.pyint(),
        )
        products.append(new_product)

    for order in orders:
        for _ in range(3):
            repo.add_product_to_order(
                product_id=random.choice(products).product_id,
                order_id=order.order_id,
                quantity=fake.pyint(),
            )

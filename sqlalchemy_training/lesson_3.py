"""Third:

- Insert queries using ORM.
- Advanced Select queries.
- Combining Insert, Select and Update in a Single Query
"""

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from sqlalchemy_training.lesson_1 import session_maker
from sqlalchemy_training.lesson_2 import User


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
    ) -> None:
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
            .returning(User)
            .on_conflict_do_update(
                index_elements=[User.telegram_id],
                set_={
                    "user_name": username,
                    "full_name": full_name,
                },
            )
        )

        result = self.session.scalars(stmt).first()
        self.session.commit()

        return result

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
        result = self.session.execute(stmt)
        self.session.commit()

        return result.scalars().all()

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


if __name__ == "__main__":
    with session_maker() as session:
        repo = Repo(session)

        # repo.add_user(
        #     telegram_id=1,
        #     full_name="Nhat Tai NGUYEN",
        #     lang="fr",
        #     username="Darth Glorious",
        # )

        user = repo.get_user_by_id(1)
        print(user)

        users = repo.get_last_ten_users()
        print(users)

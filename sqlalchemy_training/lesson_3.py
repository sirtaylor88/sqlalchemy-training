"""Third:

- Insert queries using ORM.
"""

from typing import Optional

from sqlalchemy import insert
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
    ) -> None:
        """Add new user to DB."""

        stmt = insert(User).values(
            telegram_id=telegram_id,
            full_name=full_name,
            language_code=lang,
            user_name=username,
        )
        self.session.execute(stmt)
        self.session.commit()


if __name__ == "__main__":
    with session_maker() as session:
        repo = Repo(session)

        repo.add_user(
            telegram_id=1,
            full_name="Nhat Tai NGUYEN",
            lang="fr",
            username="Darth Glorious",
        )

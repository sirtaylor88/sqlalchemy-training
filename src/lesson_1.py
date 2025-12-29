"""Create DB connection."""

import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()


# * Connection string format: driver+postgresql://user:pass@host:port/dbname
url = URL.create(
    drivername="postgresql+psycopg2",  # * postgresql + library we are using (psycopg2)
    database=os.getenv("POSTGRE_DB"),
    username=os.getenv("POSTGRE_USER"),
    password=os.getenv("POSTGRE_PASSWORD"),
    host=os.getenv("POSTGRE_HOST"),
    port=os.getenv("POSTGRE_PORT"),
)
engine = create_engine(
    url,
    echo=True,  # * The engine will log all statements and other relevant infos
)

session_maker = sessionmaker(engine)

with session_maker() as session:
    session.execute(
        text("""
            CREATE TABLE users
            (
                telegram_id   BIGINT PRIMARY KEY,
                full_name     VARCHAR(255) NOT NULL,
                username      VARCHAR(255),
                language_code VARCHAR(255) NOT NULL,
                created_at    TIMESTAMP DEFAULT NOW(),
                referrer_id   BIGINT,
                FOREIGN KEY (referrer_id)
                    REFERENCES users (telegram_id)
                    ON DELETE SET NULL
            );

            INSERT INTO users
                (telegram_id, full_name, username, language_code, created_at)
            VALUES (1, 'Peter Pan', 'peter', 'en', '2025-12-29');

            INSERT INTO users
                (telegram_id, full_name, username, language_code, created_at, referrer_id)
            VALUES (2, 'Adam Evan', 'adam', 'en', '2025-12-29', 1);
        """)
    )

    session.commit()

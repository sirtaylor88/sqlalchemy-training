"""First lesson:

- Create DB connection.
- Create a table.
- Select columns from table.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

database_url = URL.create(
    drivername="postgresql+psycopg2",  # * postgresql + library we are using (psycopg2)
    database=os.getenv("POSTGRES_DB"),
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
)

engine = create_engine(database_url, echo=True)
session_maker = sessionmaker(engine)

with session_maker() as session:
    # session.execute(
    #     text("""
    #         CREATE TABLE users
    #         (
    #             telegram_id   BIGINT PRIMARY KEY,
    #             full_name     VARCHAR(255) NOT NULL,
    #             username      VARCHAR(255),
    #             language_code VARCHAR(255) NOT NULL,
    #             created_at    TIMESTAMP DEFAULT NOW(),
    #             referrer_id   BIGINT,
    #             FOREIGN KEY (referrer_id)
    #                 REFERENCES users (telegram_id)
    #                 ON DELETE SET NULL
    #         );

    #         INSERT INTO users
    #             (telegram_id, full_name, username, language_code, created_at)
    #         VALUES (1, 'Peter Pan', 'peter', 'en', '2025-12-29');

    #         INSERT INTO users
    #             (telegram_id, full_name, username, language_code, created_at, referrer_id)
    #         VALUES (2, 'Adam Evan', 'adam', 'en', '2025-12-29', 1);
    #     """)
    # )

    # session.commit()

    result = session.execute(
        text("""
            SELECT * FROM users;
        """)
    )

    rows = result.all()

    for row in rows:
        print(row)

    result = session.execute(
        text("""
            SELECT full_name FROM users WHERE telegram_id =:telegram_id;
        """).params(telegram_id=1)
    )

    rows = result.scalars()

    for row in rows:
        print(row)

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
    session.execute(text("SELECT 1"))
    session.commit()

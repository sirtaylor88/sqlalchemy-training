"""First lesson:

- Create DB connection.
- Create a table.
- Select columns from table.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
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

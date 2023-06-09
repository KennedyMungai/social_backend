"""A file that contains the database logic for the project"""
import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ENV = load_dotenv(find_dotenv())

MYSQL_USERNAME = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")


DB_URL = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@localhost:3306/{MYSQL_DATABASE}"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """The database dependency

    Yields:
        Session: The database session
    """
    _db = SessionLocal()

    try:
        yield _db
    finally:
        _db.close()


Base = declarative_base()

"""Database initialization."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from padel_handler.utils.secrets_manager import secrets


DB_USER = secrets.get("DB_USER")
DB_PASS = secrets.get("DB_PASSWORD")
DB_HOST = secrets.get("DB_HOST")
DB_PORT = secrets.get("DB_PORT")
DB_NAME = secrets.get("DB_NAME")
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Yield a database session and then close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

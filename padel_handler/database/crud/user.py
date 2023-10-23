"""User CRUD operations."""

from sqlalchemy.orm import Session, lazyload

from padel_handler.models.user import User
from padel_handler.schemas.user_match import UserCreate
from padel_handler.config.security import get_password_hash


def get_user_by_email_query(db: Session, email: str) -> User:
    """Get a user instance from its email address."""
    return db.query(
        User
    ).options(
        lazyload(User.matches),
        lazyload(User.availabilities)
    ).filter(
        User.email == email
    ).first()


def get_user_by_id_query(db: Session, user_id: int) -> User:
    """Get a user instance from its ID."""
    return db.query(
        User
    ).options(
        lazyload(User.matches),
        lazyload(User.availabilities)
    ).filter(
        User.id == user_id
    ).first()


def create_user_query(db: Session, user: UserCreate) -> User:
    """Create a new user row in users table."""
    db_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user_query(db: Session, user_id: int) -> bool:
    db.query(User).filter(User.id == user_id).delete()
    db.commit()

    return True

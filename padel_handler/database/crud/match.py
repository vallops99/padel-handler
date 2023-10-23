"""Match CRUD operations."""

from datetime import datetime
from sqlalchemy.orm import Session, lazyload

from padel_handler.models.user import User
from padel_handler.models.match import Match


def read_match_by_id_query(
    db: Session,
    match_id: int,
    user_id: int
) -> Match | None:
    """Get a match by its ID and user ID."""
    return db.query(
        Match
    ).options(
        lazyload(Match.users)
    ).filter(
        Match.id == match_id,
        Match.users.any(id=user_id)
    ).first()


def create_match_query(
    db: Session,
    date_hour: datetime,
    users: list[User]
) -> Match:
    """Create a new match instance in matches table."""

    db_match = Match(date_hour=date_hour)
    db_match.users.extend(users)

    db.add(db_match)
    db.commit()
    db.refresh(db_match)

    return db_match


def remove_match_from_user_query(
    db: Session,
    user: User,
    match: Match
) -> Match:
    """"Remove a match from user table."""
    user.matches.remove(match)

    db.query(Match).filter(Match.id == match.id).delete()

    db.commit()

    return match


def remove_match_by_date_hour_query(
    db: Session,
    user: User,
    date_hour: datetime
) -> Match | None:
    match_q = db.query(
        Match
    ).filter(
        Match.date_hour == date_hour,
        Match.users.any(id=user.id)
    )

    match = match_q.first()
    if not match:
        return

    user.matches.remove(match)
    match_q.delete()

    db.commit()

    return match

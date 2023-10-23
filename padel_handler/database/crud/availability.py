"""Availabilities CRUD operations."""

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import insert, update

from padel_handler.models.availability import Availability

from padel_handler.schemas.availability import AvailabilityCreate


def create_availabilities_query(
    db: Session,
    availabilities: list[AvailabilityCreate],
    user_id: int
):
    """Create a new availability of a user."""
    db.execute(
        insert(Availability),
        [{**item.model_dump(), "user_id": user_id} for item in availabilities]
    )

    db.commit()


def delete_availability_query(
    db: Session,
    availability_id: int,
    user_id: int
) -> Availability | None:
    """Delete an availability by its ID and user ID."""
    availability_q = db.query(
        Availability
    ).filter(
        Availability.user.has(id=user_id),
        Availability.id == availability_id
    )

    availability = availability_q.first()
    availability_q.delete()

    db.commit()
    return availability


def delete_availability_by_date_hour_query(
    db: Session,
    date_hour: datetime,
    user_id: int
) -> Availability | None:
    """Delete an availability by date_hour and user ID."""
    availability = db.query(
        Availability
    ).filter(
        Availability.user.has(id=user_id),
        Availability.date_hour == date_hour
    )

    availability.delete()

    db.commit()

    return availability.first()


def read_matching_query(
    db: Session,
    date_hour: datetime
) -> list[Availability]:
    """
    Get all availabilities with the same date_hour as input list's values.
    """
    return db.query(Availability).filter(
        Availability.date_hour == date_hour,
        Availability.matched is False
    ).all()


def flag_availability_matched_query(
    db: Session,
    availabilities: list[Availability]
):
    """Update availability `matched` flag column to true."""
    db.execute(
        update(
            Availability
        ).where(
            Availability.id.in_([av.id for av in availabilities])
        ).values(matched=True)
    )

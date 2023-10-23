from sqlalchemy.orm import relationship
from sqlalchemy import (
    ForeignKey, Column, Integer, DateTime, UniqueConstraint, Boolean
)

from padel_handler.database.database import Base


class Availability(Base):
    """Availability table."""
    __tablename__ = "availabilities"

    id = Column(Integer, primary_key=True, index=True)
    date_hour = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    matched = Column(Boolean, default=False)

    user = relationship("User", back_populates="availabilities")

    __table_args__ = (
        UniqueConstraint('date_hour', 'user_id', name='user_availability'),
    )

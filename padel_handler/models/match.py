from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime

from padel_handler.database.database import Base
from padel_handler.models.user import association_table


class Match(Base):
    """Match table."""
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    date_hour = Column(DateTime)

    users = relationship(
        "User",
        secondary=association_table,
        back_populates="matches"
    )

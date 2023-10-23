from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Boolean

from padel_handler.database.database import Base


association_table = Table(
    "cross_users_matches",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("match_id", ForeignKey("matches.id", ondelete="CASCADE")),
)


class User(Base):
    """User table."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    availabilities = relationship("Availability", back_populates="user")
    matches = relationship(
        "Match",
        secondary=association_table,
        back_populates="users",
        cascade="delete"
    )

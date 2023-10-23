"""User pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict

from padel_handler.schemas.availability import Availability


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserLazy(UserBase):
    model_config = ConfigDict(from_attribute=True)

    id: int
    is_active: bool


class MatchBase(BaseModel):
    date_hour: datetime


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    model_config = ConfigDict(from_attribute=True)

    id: int

    users: list["UserLazy"] = []


class User(UserBase):
    model_config = ConfigDict(from_attribute=True)

    id: int

    is_active: bool

    matches: list["Match"] = []
    availabilities: list[Availability] = []


class UserInDB(UserBase):
    hashed_password: str

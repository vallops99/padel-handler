"""Availability pydantic schemas."""

from datetime import datetime
from pydantic import (
    BaseModel, ConfigDict, FutureDatetime, model_validator, validator
)

from padel_handler.utils.enum import Date


def date_hour_to_datetime(date_hour: str) -> datetime:
    """Transform stringed date into a date."""
    return datetime.strptime(
        date_hour,
        Date.FORMAT.value
    )


def date_hour_to_str(date_hour: datetime) -> str:
    return date_hour.strftime(Date.FORMAT.value)


class AvailabilityBase(BaseModel):
    date_hour: FutureDatetime


class AvailabilityCreate(AvailabilityBase):
    _extract_date_hour = validator(
        'date_hour',
        pre=True,
        allow_reuse=True
    )(date_hour_to_datetime)

    @model_validator(mode="after")
    def validate_after(self) -> AvailabilityBase:
        assert (
            self.date_hour.hour >= 9
        ), "availability date field start from 9 AM (date_hour)"
        assert (
            self.date_hour.hour <= 23
        ), "availability date field ends at 11 PM (date_hour)"

        return self


class Availability(AvailabilityBase):
    model_config = ConfigDict(from_attribute=True)

    id: int
    user_id: int
    date_hour: str

    _extract_date_hour = validator(
        'date_hour',
        pre=True,
        allow_reuse=True
    )(date_hour_to_str)

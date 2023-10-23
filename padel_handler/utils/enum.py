"""Project enums."""

from enum import Enum


class CustomEnum(Enum):
    """Base of enums with get_vals method."""
    def __str__(self):
        return self.value

    @classmethod
    def get_vals(cls):
        """Get a list of the enum values."""
        return [x.value for x in cls]

    @classmethod
    def get_dict_vals(cls):
        """Get a dict of the enum values."""
        return {x.name: x.value for x in cls}


class AWS(CustomEnum):
    """AWS enums."""
    REGION_NAME = 'eu-west-1'


class Security(CustomEnum):
    """Security enums."""
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Date(CustomEnum):
    FORMAT = "%Y-%m-%d %H"


class MatchConfig(CustomEnum):
    PLAYER_NUMBER = 4

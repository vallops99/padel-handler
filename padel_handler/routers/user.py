from typing import Annotated, Literal
from fastapi import Depends, APIRouter

from padel_handler.models.user import User as UserModel
from padel_handler.schemas.availability import Availability
from padel_handler.schemas.user_match import UserLazy, Match
from padel_handler.database.crud.user import delete_user_query
from padel_handler.database.database import SessionLocal, get_db
from padel_handler.utils.utils import (
    get_active_user_from_token, get_user_from_token
)


router = APIRouter(prefix="/users")


@router.get("/me/", response_model=UserLazy)
async def get_user_detail(
    user: Annotated[UserModel, Depends(get_user_from_token)]
):
    return user


@router.delete("/me/")
async def delete_user(
    user: Annotated[UserModel, Depends(get_user_from_token)],
    db: Annotated[SessionLocal, Depends(get_db)]
) -> dict[Literal["message"], Literal["User deleted!"]]:
    delete_user_query(db, user.id)

    return {"message": "User deleted!"}


@router.get("/me/availabilities/", response_model=list[Availability])
async def get_user_availabilities(
    user: Annotated[UserModel, Depends(get_active_user_from_token)],
):
    return user.availabilities


@router.get("/me/matches/", response_model=list[Match])
async def get_user_matches(
    user: Annotated[UserModel, Depends(get_active_user_from_token)]
):
    return user.matches

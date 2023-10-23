from typing import Annotated, Literal
from fastapi import Depends, HTTPException, APIRouter, BackgroundTasks

from padel_handler.models.user import User
from padel_handler.schemas.user_match import Match, MatchBase
from padel_handler.config.security import oauth2_scheme
from padel_handler.database.database import SessionLocal, get_db
from padel_handler.utils.utils import (
    get_active_user_from_token, remove_availability
)
from padel_handler.database.crud.match import (
    read_match_by_id_query, remove_match_from_user_query
)


router = APIRouter(
    prefix="/matches",
    dependencies=[Depends(oauth2_scheme)]
)


@router.get("/{match_id}/", response_model=Match)
async def get_match_detail(
    match_id: int,
    user: Annotated[User, Depends(get_active_user_from_token)],
    db: Annotated[SessionLocal, Depends(get_db)]
):
    match = read_match_by_id_query(db, match_id, user.id)
    if not match:
        raise HTTPException(
            status_code=404,
            detail="Requested match not found."
        )

    return match


@router.delete("/{match_id}/", response_model=MatchBase)
async def delete_match(
    match_id: int,
    user: Annotated[User, Depends(get_active_user_from_token)],
    db: Annotated[SessionLocal, Depends(get_db)],
    background_task: BackgroundTasks
) -> dict[Literal["deleted"], bool]:
    match = read_match_by_id_query(db, match_id, user.id)

    if match:
        # Get users before match is no more bound to a Session.
        match_users = match.users

        remove_match_from_user_query(db, user, match)
        background_task.add_task(
            remove_availability,
            db,
            match,
            user.id,
            match_users
        )
    else:
        raise HTTPException(
            status_code=404,
            detail="Match not found!"
        )

    return match

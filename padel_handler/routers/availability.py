from typing import Annotated, Literal
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, APIRouter, BackgroundTasks, HTTPException, status

from padel_handler.models.user import User
from padel_handler.database.database import SessionLocal, get_db
from padel_handler.schemas.availability import AvailabilityCreate, Availability
from padel_handler.database.crud.availability import (
    create_availabilities_query, delete_availability_query
)
from padel_handler.utils.utils import (
    create_matches_of_user, get_active_user_from_token, remove_match
)


router = APIRouter(prefix="/availabilities")


@router.post("/")
async def create_availabilities(
    availabilities_data: list[AvailabilityCreate],
    user: Annotated[User, Depends(get_active_user_from_token)],
    db: Annotated[SessionLocal, Depends(get_db)],
    background_task: BackgroundTasks
) -> dict[Literal["created"], bool]:
    try:
        create_availabilities_query(
            db,
            availabilities_data,
            user.id
        )
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error while creating availabilities: {err.orig}"
        )

    background_task.add_task(create_matches_of_user, db, user)

    return {"created": True}


@router.delete("/{availability_id}/", response_model=Availability)
async def delete_availability(
    availability_id: int,
    user: Annotated[User, Depends(get_active_user_from_token)],
    db: Annotated[SessionLocal, Depends(get_db)],
    background_task: BackgroundTasks
) -> dict[Literal["deleted"], bool]:
    availability = delete_availability_query(
        db,
        availability_id,
        user.id
    )

    if availability:
        background_task.add_task(
            remove_match,
            db,
            user,
            availability.date_hour
        )
    else:
        raise HTTPException(
            status_code=404,
            detail="Availability not found!"
        )

    return availability

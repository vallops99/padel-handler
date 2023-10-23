from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException

from padel_handler.schemas.auth import Token
from padel_handler.utils.enum import Security
from padel_handler.schemas.user_match import User, UserCreate
from padel_handler.database.database import SessionLocal, get_db
from padel_handler.config.security import create_jwt_token, verify_password
from padel_handler.database.crud.user import (
    create_user_query, get_user_by_email_query
)


router = APIRouter()


@router.post("/signup/", response_model=User)
async def signup(
    user_data: UserCreate,
    db: Annotated[SessionLocal, Depends(get_db)]
):
    return create_user_query(db, user_data)


@router.post("/signin/", response_model=Token)
async def signin(
    user_data: UserCreate,
    db: Annotated[SessionLocal, Depends(get_db)]
):
    user = get_user_by_email_query(db, user_data.email)
    if not user or not verify_password(
        user_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Email or password not matching a user!",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_jwt_token(
        data={"email": user.email}, expires_delta=timedelta(
            minutes=Security.ACCESS_TOKEN_EXPIRE_MINUTES.value
        )
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )

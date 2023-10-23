"""Project utilities."""

import os
from typing import Annotated
from datetime import datetime
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from padel_handler.models.match import Match

from padel_handler.models.user import User
from padel_handler.config.security import oauth2_scheme
from padel_handler.utils.secrets_manager import secrets
from padel_handler.utils.enum import Date, MatchConfig, Security
from padel_handler.database.database import SessionLocal, get_db
from padel_handler.database.crud.user import get_user_by_email_query
from padel_handler.database.crud.match import (
    create_match_query, remove_match_by_date_hour_query
)
from padel_handler.database.crud.availability import (
    delete_availability_by_date_hour_query, flag_availability_matched_query,
    read_matching_query
)


mail_conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
    MAIL_FROM=os.environ.get("MAIL_FROM"),
    MAIL_PORT=int(os.environ.get("MAIL_PORT")),
    MAIL_SERVER=os.environ.get("MAIL_SERVER"),
    MAIL_FROM_NAME=os.environ.get("MAIN_FROM_NAME"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="./templates/email"
)


async def get_user_from_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[SessionLocal, Depends(get_db)]
) -> User:
    """Retrieve email from access token."""
    try:
        payload = jwt.decode(
            token,
            secrets.get("SECRET_KEY"),
            algorithms=[Security.ALGORITHM.value]
        )
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token can not be decoded.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    user = get_user_by_email_query(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


async def get_active_user_from_token(
    user: Annotated[User, Depends(get_user_from_token)]
) -> User:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user


async def create_matches_of_user(db: SessionLocal, user: User):
    """
    Check if there are 4 availabilities at the same date-hour,
    if so create a match.
    """
    filter_av = filter(
        lambda av: av.date_hour > datetime.now(),
        user.availabilities
    )
    for availability in filter_av:
        matching_availabilities = read_matching_query(
            db,
            availability.date_hour
        )

        if len(matching_availabilities) < MatchConfig.PLAYER_NUMBER.value:
            continue

        users = [av.user for av in matching_availabilities]
        create_match_query(
            db,
            availability.date_hour,
            users
        )
        flag_availability_matched_query(
            db,
            [availability, *matching_availabilities]
        )
        await send_emails(
            "Match available!",
            [u.email for u in users],
            "A match has been created based on your availabilities!"
            "Match date: " + availability.date_hour.strftime(Date.FORMAT.value),
            template='match_created.html'
        )


async def remove_match(
    db: SessionLocal,
    user: User,
    date_hour: datetime
):
    match = remove_match_by_date_hour_query(db, user, date_hour)
    if match:
        await send_emails(
            "Match deleted!",
            [u.email for u in match.users],
            "A match of yours has been deleted!"
            "Match date: " + date_hour.strftime(Date.FORMAT.value),
            template='match_deleted.html'
        )


async def remove_availability(
    db: SessionLocal,
    match: Match,
    user_id: int,
    match_users: list[User]
):
    delete_availability_by_date_hour_query(db, match.date_hour, user_id)
    await send_emails(
        "Match deleted!",
        [u.email for u in match_users],
        "A match of yours has been deleted!"
        "Match date: " + match.date_hour.strftime(Date.FORMAT.value),
        template='match_deleted.html'
    )


async def send_emails(
    subject: str,
    mails: list[str],
    body: dict,
    template: str
):
    message = MessageSchema(
        subject=subject,
        recipients=mails,
        body=body,
        subtype='html',
    )

    fm = FastMail(mail_conf)
    await fm.send_message(message, template_name=template)

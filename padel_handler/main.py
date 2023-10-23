"""Project main module."""

from typing import Literal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from padel_handler.routers.auth import router as auth_router
from padel_handler.routers.user import router as user_router
from padel_handler.routers.match import router as match_router
from padel_handler.routers.availability import router as availability_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(match_router)
app.include_router(availability_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "*"],
    expose_headers=["Date", "x-api-id"],
    max_age=300
)


@app.get("/")
async def root() -> dict[Literal["message"], Literal["Padel handler developed by Valerio Farrotti."]]:
    return {"message": "Padel handler developed by Valerio Farrotti."}


# This is a lambda handler in case we want to use an
# API Gateway with lambdas.
# handler = Mangum(app)

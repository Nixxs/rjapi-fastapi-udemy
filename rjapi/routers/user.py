import logging

from fastapi import APIRouter, HTTPException

from rjapi.database import database, user_table
from rjapi.models.user import UserIn
from rjapi.security import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register", status_code=201)
async def register(user: UserIn):
    # if a user is returned then the email aready exists
    if await get_user(user.email):
        raise HTTPException(
            status_code=400, detail="A user with that email already exists"
        )

    hashed_password = get_password_hash(user.password)

    query = user_table.insert().values(email=user.email, password=hashed_password)
    logger.debug(query)

    await database.execute(query)

    return {"detail": "User Created."}


@router.post("/token", status_code=200)
async def login(user: UserIn):
    user = await authenticate_user(user.email, user.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}

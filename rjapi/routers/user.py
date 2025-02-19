import logging

from fastapi import APIRouter, HTTPException

from rjapi.database import database, user_table
from rjapi.models.user import UserIn
from rjapi.security import get_user

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register", status_code=201)
async def register(user: UserIn):
    # if a user is returned then the email aready exists
    if await get_user(user.email):
        raise HTTPException(
            status_code=400, detail="A user with that email already exists"
        )

    query = user_table.insert().values(email=user.email, password=user.password)
    logger.debug(query)

    await database.execute(query)

    return {"detail": "User Created."}

from sqlalchemy import select, or_
from fastapi import HTTPException
from passlib.context import CryptContext
from .models import Users
from .shemas import UserBase

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def conflict_user(userData, session):
    filters = [Users.email == userData.email, Users.username == userData.username]
    query = select(Users).where(or_(*filters))
    if (await session.execute(query)).scalar():
        raise HTTPException(status_code=409, detail="User already exists")


async def register_user(userData, session):
    await conflict_user(userData, session)

    hash_password = password_context.hash(userData.password)
    userOrm = Users(email=userData.email, username=userData.username, hash_password=hash_password)
    session.add(userOrm)
    await session.flush()
    user = UserBase.model_validate(userOrm, from_attributes=True)
    await session.commit()
    return user

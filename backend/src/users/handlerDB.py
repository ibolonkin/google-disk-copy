from sqlalchemy import select, or_, orm

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
    hash_password = password_context.hash(userData.password)
    userOrm = Users(email=userData.email, username=userData.username, hash_password=hash_password)
    session.add(userOrm)
    await session.flush()
    user = userOrm
    await session.commit()
    return user

def get_find(obj_type: orm.attributes.InstrumentedAttribute):
    async def find(obj, session):
        query = select(Users).where(obj_type == obj)
        user = (await session.execute(query)).scalar()
        return user

    return find


find_sub = get_find(Users.uuid)
find_email = get_find(Users.email)

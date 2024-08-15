from fastapi import Depends, APIRouter, status

from .utils import (get_current_auth_user, validate_auth_user,
                    get_current_auth_user_refresh, return_token)
from ..base import get_async_session
from .shemas import UserRegister, UserBase, Token
from .handlerDB import register_user

router = APIRouter()


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(userData: UserRegister, session=Depends(get_async_session)) -> Token:
    user: UserBase = await register_user(userData, session)
    return return_token(user)


@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserBase)
async def get_my_info(user: UserBase = Depends(get_current_auth_user)):
    return user


@router.post('/auth', status_code=status.HTTP_200_OK)
async def auth(user: UserBase = Depends(validate_auth_user)) -> Token:
    return return_token(user)


@router.post('/refresh', status_code=status.HTTP_200_OK)
async def refresh(user: UserBase = Depends(get_current_auth_user_refresh)) -> Token:
    return return_token(user)

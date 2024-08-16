from fastapi import Depends, APIRouter, status, Response, HTTPException

from .utils import (validate_auth_user,
                    return_token, get_auth_user_refresh, get_current_auth_user_active, get_current_auth_user)
from ..base import get_async_session
from .shemas import UserRegister, UserBase, Token
from .handlerDB import register_user

router = APIRouter()


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(response: Response, userData: UserRegister, session=Depends(get_async_session)) -> Token:
    user: UserBase = await register_user(userData, session)
    return return_token(user, response)


@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserBase)
async def get_my_info(user: UserBase = Depends(get_current_auth_user_active)):
    return user


@router.post('/auth', status_code=status.HTTP_200_OK)
async def auth(response: Response, user: UserBase = Depends(validate_auth_user)) -> Token:
    return return_token(user, response)


# TODO: ничего не понятно с удалением пользователя когда ему восстанавливаться и где и можно ли ему в рефреш
@router.post('/refresh', status_code=status.HTTP_200_OK)
async def refresh(response: Response, user: UserBase = Depends(get_auth_user_refresh)) -> Token:
    return return_token(user, response)


@router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete_user(user=Depends(get_current_auth_user_active), session=Depends(get_async_session)):
    user.active = False
    await session.commit()
    return {'message': 'User deleted'}


@router.put('/restore', status_code=status.HTTP_200_OK)
async def restore_user(user=Depends(get_current_auth_user), session=Depends(get_async_session)):
    user.active = True
    await session.commit()
    return {'message': 'User restore'}

from fastapi import Depends, APIRouter, HTTPException, status
from .utils import create_refresh_token, create_access_token
from ..base import get_async_session
from .shemas import UserRegister, UserBase, Token
from .handlerDB import register_user

router = APIRouter()


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(userData: UserRegister, session=Depends(get_async_session)):
    user: UserBase = await register_user(userData, session)
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )
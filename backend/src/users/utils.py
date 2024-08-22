from datetime import timedelta, datetime, timezone
import jwt
from fastapi import Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from .handlerDB import find_sub, find_email, password_context
from .shemas import UserBase, UserLogin, Token
from .models import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, VERIFY_TOKEN_TYPE
from ..base import get_async_session
from ..config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

http_bearer = HTTPBearer(auto_error=False)


def encode_jwt(
        payload: dict,
        private_key=settings.auth_jwt.private_key_path.read_text(),
        algorithm=settings.auth_jwt.algorithm,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire, 'iat': now})

    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def create_jwt(token_type: str, token_data: dict,
               expire_minutes=settings.auth_jwt.access_token_expire_minutes,
               expire_timedelta: timedelta | None = None):
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(payload=jwt_payload, expire_minutes=expire_minutes, expire_timedelta=expire_timedelta)


def create_access_token(user: UserBase) -> str:
    jwt_payload = {
        'username': user.username,
        'email': user.email,
        'sub': str(user.uuid),
        'verified': user.verified
    }
    return create_jwt(token_type=ACCESS_TOKEN_TYPE,
                      token_data=jwt_payload,
                      expire_minutes=settings.auth_jwt.access_token_expire_minutes,
                      )


def create_refresh_token(user) -> str:
    jwt_payload = {
        "sub": str(user.uuid)
    }
    return create_jwt(token_type=REFRESH_TOKEN_TYPE,
                      token_data=jwt_payload,
                      expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days))


def decode_jwt(
        token: str | bytes,
        public_key=settings.auth_jwt.public_key_path.read_text(),
        algorithm=settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    try:
        token = credentials.credentials
        payload = decode_jwt(token=token)
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token ( parse ) ')
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token not found')
    return payload


def validate_token_type(
        payload: dict,
        token_type: str,
) -> bool:
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"token invalid {token_type}"
                                                                         f" != {payload.get(TOKEN_TYPE_FIELD)}")


def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
            payload: dict = Depends(get_current_token_payload),
            session=Depends(get_async_session)
    ):
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload, session)

    return get_auth_user_from_token


async def get_user_by_token_sub(
        payload: dict,
        session: AsyncSession
):
    sub = payload.get('sub')
    if user := await find_sub(sub, session):
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid")


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)


async def get_current_auth_user_noActive(user=Depends(get_current_auth_user)):
    if not user.active:
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user is already active")


# get_current_auth_user_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)

async def get_current_auth_user_active(user=Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not active")


async def get_auth_user_refresh(request: Request, session=Depends(get_async_session)):
    token = request.cookies.get(settings.auth_jwt.key_cookie)
    try:
        payload = decode_jwt(token=token)
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token ( parse ) ')
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    return await get_user_by_token_sub(payload, session)


async def validate_auth_user(
        userData: UserLogin,
        session=Depends(get_async_session)
):
    if not (user := await find_email(userData.email, session)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='email or password wrong')
    if not password_context.verify(userData.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='email or password wrong')
    return user


def return_token(user: UserBase, response: Response):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    response.set_cookie(key=settings.auth_jwt.key_cookie, value=refresh_token, httponly=True,
                        max_age=settings.auth_jwt.refresh_token_expire_days * 24 * 60 * 60, )
    return Token(
        access_token=access_token,
    )


def create_verify_token(user: UserBase):
    jwt_payload = {
        'email': user.email,
        'sub': str(user.uuid),
    }
    return create_jwt(token_type=VERIFY_TOKEN_TYPE,
                      token_data=jwt_payload,
                      expire_minutes=settings.auth_jwt.verify_token_expire_minutes,
                      )


async def verify_mail_token(token: str, session=Depends(get_async_session)):
    try:
        payload = decode_jwt(token=token)
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token', )
    validate_token_type(payload, VERIFY_TOKEN_TYPE)
    user = await get_user_by_token_sub(payload, session)
    if user.email != payload['email']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token')
    user.verified = True
    await session.commit()
    return user

async def send_mail(user):
    url = f'http://localhost:8000/v1/confirm/{create_verify_token(user)}'
    server = smtplib.SMTP('smtp.mail.ru', 587)
    server.starttls()
    msg = MIMEMultipart()
    fromaddr = settings.EMAIL_LOGIN
    toaddr = user.email
    mypass = settings.EMAIL_PASSWORD
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Подтверждение почты"
    body = f"""
    <html>
    <body>
      <p>Перейдите по <a href='{url}'>ссылке</a>, чтобы подтвердить почту </p>
    </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    return

from pydantic import BaseModel , EmailStr, UUID4

class User(BaseModel):
    username: str
    email: EmailStr

class UserRegister(User):
    password: str

class UserBase(User):
    uuid: UUID4

class Token(BaseModel):
    token_type: str = 'Bearer'
    access_token: str
    refresh_token: str

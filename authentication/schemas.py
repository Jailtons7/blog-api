from typing import Union

from pydantic import BaseModel


class UserAddSchema(BaseModel):
    name: str
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    name: str
    username: str
    email: str

    class Config:
        from_attributes = True


class UserViewSchema(BaseModel):
    id: int
    name: str
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str

    class Config:
        from_attributes = True


class MessageSchema(BaseModel):
    message: str

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None

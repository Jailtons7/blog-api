from typing import Union
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserAddSchema(BaseModel):
    name: str
    username: str
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    name: str
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserViewSchema(BaseModel):
    id: int
    name: str
    username: str
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str

    model_config = ConfigDict(from_attributes=True)


class MessageSchema(BaseModel):
    message: str

    model_config = ConfigDict(from_attributes=True)


class LoginSchema(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
    token_expires: datetime


class TokenData(BaseModel):
    email: Union[str, None] = None

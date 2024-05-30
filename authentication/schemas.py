from typing import Union

from pydantic import BaseModel


class UserAddSchema(BaseModel):
    name: str
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UserViewSchema(BaseModel):
    name: str
    username: str
    email: str
    is_active: bool

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
    username: Union[str, None] = None

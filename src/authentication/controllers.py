from typing import List, cast, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.authentication.schemas import (
    UserAddSchema,
    UserViewSchema,
    Token,
    ChangePasswordSchema,
    MessageSchema,
    UserUpdateSchema,
    TokenVerifySchema,
    TokenVerifyResponseSchema,
)
from src.authentication.models import User
from src.authentication.token import create_access_token, verify_access_token
from src.authentication.oauth2 import get_current_user
from src.db.connection import get_db
from settings import Settings


router = APIRouter()
settings = Settings()


@router.post("/users", response_model=UserViewSchema, status_code=status.HTTP_201_CREATED)
async def add_user(user: UserAddSchema, db: Session = Depends(get_db)):
    """
    Add a new user to the database.
    """
    try:
        new_user = User(**user.dict())
        new_user.set_password(password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both username and email fields must be unique"
        )
    return new_user


@router.get("/users", response_model=List[UserViewSchema], status_code=status.HTTP_200_OK)
def list_users(user: UserViewSchema = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Retrieve all active users saved.
    """
    users = db.query(User).filter(cast("ColumnElement[bool]", User.is_active)).all()
    return users


@router.get("/users/{user_id}", response_model=UserViewSchema, status_code=status.HTTP_200_OK)
def get_user(
        user_id: int,
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)):
    """
    Retrieve a specific user with the given {user_id}.
    """
    user = db.query(User).filter(cast("ColumnElement[bool]", User.id == user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found: id {user_id}"
        )
    return user


@router.put("/users", response_model=UserUpdateSchema, status_code=status.HTTP_200_OK)
def update_user(
        data: UserUpdateSchema,
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user.name = data.name
    user.email = data.email
    user.username = data.username
    db.commit()
    db.refresh(user)
    return UserUpdateSchema(
        name=user.name,
        email=user.email,
        username=user.username
    )


@router.delete("/users", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user: UserViewSchema = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Delete the current user.
    """
    # Actually, this only deactivates the user
    user.is_active = False
    db.commit()
    db.refresh(user)
    return True


@router.patch("/users/change-password", response_model=MessageSchema, status_code=status.HTTP_200_OK)
def change_password(
        data: ChangePasswordSchema,
        user: UserViewSchema = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if user.check_password(data.old_password):
        user.set_password(password=data.new_password)
        db.commit()
        return MessageSchema(message="Password changed successfully")
    return MessageSchema(message="Your old password is not correct")


@router.post("/access-token", response_model=Token, status_code=status.HTTP_201_CREATED)
def get_access_token(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user: Union[User, None] = db.query(User).filter(
        cast("ColumnElement[bool]", User.email == user.username)
    ).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with this email: {user.username}, please create an account first"
        )

    if not db_user.check_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_expires = (datetime.now() + expires_delta).strftime("%Y-%m-%dT%H:%M:%S")
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=expires_delta
    )
    return Token(access_token=access_token, token_expires=token_expires, token_type="bearer")


@router.post("/verify-token", response_model=TokenVerifyResponseSchema, status_code=status.HTTP_201_CREATED)
async def verify_token(data: TokenVerifySchema):
    try:
        verify_access_token(token=data.token)
        return TokenVerifyResponseSchema(valid=True)
    except HTTPException as e:
        print(e)
        return TokenVerifyResponseSchema(valid=False)

from typing import Annotated, cast, Type

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from settings import Settings
from authentication.token import verify_access_token
from authentication.models import User
from db.connection import get_db


settings = Settings()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"auth/access-token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> Type[User]:
    verification = verify_access_token(token=token)
    email = verification.email
    user = db.query(User).filter(cast("ColumnElement[bool]", User.email == email)).first()
    return user

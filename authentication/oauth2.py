from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from settings import Settings
from authentication.token import verify_access_token

settings = Settings()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"auth/access-token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return verify_access_token(token=token)

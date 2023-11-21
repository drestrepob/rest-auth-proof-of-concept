from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Annotated

from app.config import settings

bearer_scheme = HTTPBearer()
expiration = datetime.now() + timedelta(seconds=20)


async def authenticate_bearer(token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]):
    if token.credentials != settings.BEARER_TOKEN:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if datetime.now() > expiration:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token.credentials

import secrets

from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config import settings

security = HTTPBasic()


def validate_credentials(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    encoded_username = credentials.username.encode("utf8")
    encoded_password = credentials.password.encode("utf8")
    expected_username = settings.BASIC_USERNAME.encode("utf8")
    expected_password = settings.BASIC_PASSWORD.encode("utf8")

    is_correct_username = secrets.compare_digest(encoded_username, expected_username)
    is_correct_password = secrets.compare_digest(encoded_password, expected_password)
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"}
        )

    return credentials.username

import hashlib
import logging

from fastapi import Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPDigest
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Annotated

from app.config import settings
from app.schemas import HTTPDigestCredentials


logger = logging.getLogger(__name__)
security = HTTPDigest()


def _get_expected_response(username: str, password: str, realm: str, nonce: str, uri: str, method="GET") -> str:
    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()
    ha2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
    response = hashlib.md5(f"{ha1}:{nonce}:{ha2}".encode()).hexdigest()
    return response


def validate_credentials(credentials: Annotated[HTTPAuthorizationCredentials, Security(security)]):
    parsed_credentials = HTTPDigestCredentials.from_string_credentials(credentials.credentials)
    username = settings.DIGEST_USERNAME
    password = settings.DIGEST_PASSWORD
    expected_response = _get_expected_response(
        username=username,
        password=password,
        realm=parsed_credentials.realm,
        nonce=parsed_credentials.nonce,
        uri=parsed_credentials.uri,
    )
    if parsed_credentials.response != expected_response:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Digest"}
        )

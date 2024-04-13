import httpx
import logging

from typing import Annotated, Final

import jwt

from fastapi import HTTPException, Security
from fastapi.security.oauth2 import OAuth2, OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from starlette import status
from starlette.requests import Request

from app.config import settings

logger = logging.getLogger(__name__)
base_url: Final[str] = f"https://{settings.AUTH0_DOMAIN}"
jwks_client = jwt.PyJWKClient(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
default_headers: dict[str, str] = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "no-cache"
}
jwks_url: Final[str] = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"


class OAuth2ClientCredentials(OAuth2):
    """
    Implement OAuth2 client_credentials workflow.

    This is modeled after the OAuth2PasswordBearer and OAuth2AuthorizationCodeBearer
    classes from FastAPI, but sets auto_error to True to avoid uncovered branches.
    See https://github.com/tiangolo/fastapi/issues/774 for original implementation,
    and to check if FastAPI added a similar class.

    See RFC 6749 for details of the client credentials authorization grant.
    """
    def __init__(self, token_url: str, scheme_name: str | None = None, scopes: dict[str, str] | None = None):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(clientCredentials={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=True)

    async def __call__(self, request: Request) -> str | None:
        authorization: str | None = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return param


oauth2_scheme = OAuth2ClientCredentials(token_url="/auth0/token")


def retrieve_token(client_id: str, client_secret: str) -> dict:
    """Generates an access token for the client.

    Args:
        client_id: The client ID.
        client_secret: The client secret.

    Returns:
        The access token and its metadata.

    Raises:
        AuthenticationError: If the credentials are invalid.
    """
    payload: dict[str, str] = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": settings.AUTH0_AUDIENCE,
    }
    response = httpx.post(url=f"{base_url}/oauth/token", headers=default_headers, data=payload)
    if response.status_code != status.HTTP_200_OK:
        logger.error(f"AUTH0 response: {response.json()}")
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json(),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return response.json()


async def validate_token(token: Annotated[str, Security(oauth2_scheme)]) -> dict:
    """Validates the token and returns the payload if valid.

    Args:
        token: The token to validate.

    Returns:
        The decoded payload of the token.

    Raises:
        AuthenticationError: If the token is invalid.
    """
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token).key
    except (jwt.exceptions.PyJWKClientError, jwt.exceptions.DecodeError):
        logger.exception("Error getting signing key!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=settings.AUTH0_MANAGEMENT_AUDIENCE,
            issuer=settings.AUTH0_MANAGEMENT_ISSUER,
        )
    except (jwt.ExpiredSignatureError, jwt.PyJWTError):
        logger.exception("Error decoding token!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload

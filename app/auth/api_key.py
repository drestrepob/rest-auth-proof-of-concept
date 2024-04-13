from typing import Annotated

from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config import settings

api_key_query = APIKeyQuery(name=settings.API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_qp: Annotated[str, Security(api_key_query)],
    api_key_h: Annotated[str, Security(api_key_header)],
):
    if api_key_qp == settings.API_KEY:
        return api_key_query
    elif api_key_h == settings.API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate API KEY"
        )

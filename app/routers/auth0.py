from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from app.auth.auth0 import retrieve_token, validate_token


router = APIRouter(
    prefix='/auth0',
    tags=['OAuth2'],
    responses={status.HTTP_404_NOT_FOUND: {'description': 'Not found'}},
)


@router.get('/resources')
async def get_items(valid_token: Annotated[dict, Depends(validate_token)]):
    return {
        'message': 'You are accessing these resources using Auth0!',
        'payload': valid_token
    }


@router.post('/token')
async def login_for_token(credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]):
    token = retrieve_token(client_id=credentials.username, client_secret=credentials.password)
    return token.get("access_token")
